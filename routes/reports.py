import os
import uuid

from flask import (
    Blueprint, render_template, request, redirect, url_for, flash,
    current_app, abort
)
from flask_login import current_user
from werkzeug.utils import secure_filename

from models.models import db, Report, ReportStatusHistory, Notification
from utils.decorators import login_required
from services.duplicate_detection import find_duplicate, merge_into
from services.priority import recalculate_priority
from services.ai_suggestion import suggest_from_image

bp = Blueprint("reports", __name__, url_prefix="/reports")

DAMAGE_TYPES = [
    ("pothole", "Pothole"),
    ("crack", "Road crack"),
    ("sign", "Broken traffic sign"),
    ("road_damage", "Damaged road"),
    ("streetlight", "Broken street light"),
]
SEVERITIES = [
    ("low", "Low"), ("medium", "Medium"), ("high", "High"), ("critical", "Critical"),
]

STATUS_LABELS = {
    "new": "New",
    "verified": "Verified",
    "assigned": "Officer assigned",
    "under_repair": "Under repair",
    "completed": "Repair completed - awaiting your confirmation",
    "resolved_confirmed": "Resolved (confirmed)",
    "rejected": "Rejected",
}


def _allowed_file(filename):
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def _notify(user_id, report_id, message):
    new_notif = Notification(user_id=user_id, report_id=report_id, message=message)
    db.session.add(new_notif)
    db.session.commit()


@bp.route("/new", methods=["GET", "POST"])
@login_required
def new_report():
    if request.method == "POST":
        damage_type = request.form.get("damage_type")
        severity = request.form.get("severity")
        description = request.form.get("description", "").strip()
        latitude = request.form.get("latitude")
        longitude = request.form.get("longitude")
        address_hint = request.form.get("address_hint", "").strip()

        errors = []
        if damage_type not in dict(DAMAGE_TYPES):
            errors.append("Please select a valid damage type.")
        if severity not in dict(SEVERITIES):
            errors.append("Please select a valid severity.")
        try:
            latitude = float(latitude)
            longitude = float(longitude)
            if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
                raise ValueError
        except (TypeError, ValueError):
            errors.append("A valid GPS location is required. Please allow location access.")

        if errors:
            for e in errors:
                flash(e, "danger")
            return render_template(
                "report_form.html", damage_types=DAMAGE_TYPES, severities=SEVERITIES, form=request.form
            )

        # Handle optional photo upload
        image_path = None
        file = request.files.get("photo")
        if file and file.filename and _allowed_file(file.filename):
            ext = file.filename.rsplit(".", 1)[-1].lower()
            fname = f"{uuid.uuid4().hex}.{ext}"
            fname = secure_filename(fname)
            full_path = os.path.join(current_app.config["UPLOAD_FOLDER"], fname)
            file.save(full_path)
            image_path = f"images/reports/{fname}"

        # --- Duplicate detection ---
        duplicate = find_duplicate(latitude, longitude, damage_type)
        if duplicate:
            merge_into(duplicate.id)
            new_report = Report(
                user_id=current_user.id,
                damage_type=damage_type,
                description=description,
                severity=severity,
                latitude=latitude,
                longitude=longitude,
                address_hint=address_hint,
                image_path=image_path,
                status='new',
                duplicate_of=duplicate.id
            )
            db.session.add(new_report)
            db.session.commit()
            
            flash(
                "A similar issue has already been reported nearby. "
                "We've linked your report to the existing one to speed up its resolution.",
                "info",
            )
            return redirect(url_for("reports.my_reports"))

        # --- Optional AI suggestion (advisory only, doesn't override user's choice) ---
        ai_type, ai_severity, ai_reasoning = None, None, None
        if image_path:
            suggestion = suggest_from_image(
                os.path.join(current_app.config["UPLOAD_FOLDER"], os.path.basename(image_path))
            )
            if suggestion:
                ai_type = suggestion["damage_type"]
                ai_severity = suggestion["severity"]
                ai_reasoning = suggestion.get("ai_reasoning")

        new_report = Report(
            user_id=current_user.id,
            damage_type=damage_type,
            description=description,
            severity=severity,
            latitude=latitude,
            longitude=longitude,
            address_hint=address_hint,
            image_path=image_path,
            status='new',
            ai_suggested_type=ai_type,
            ai_suggested_severity=ai_severity,
            ai_reasoning=ai_reasoning
        )
        db.session.add(new_report)
        db.session.commit()
        report_id = new_report.id
        recalculate_priority(report_id)
        flash("Report submitted. Thank you for helping improve our roads!", "success")
        return redirect(url_for("reports.my_reports"))

    return render_template(
        "report_form.html", damage_types=DAMAGE_TYPES, severities=SEVERITIES, form={}
    )


@bp.route("/mine")
@login_required
def my_reports():
    rows = Report.query.filter_by(user_id=current_user.id).order_by(Report.created_at.desc()).all()
    return render_template("my_reports.html", reports=rows, status_labels=STATUS_LABELS)


@bp.route("/<int:report_id>")
@login_required
def detail(report_id):
    report = db.session.get(Report, report_id)
    if report is None:
        abort(404)
    if report.user_id != current_user.id and current_user.role not in ("admin", "officer"):
        abort(403)
    history = ReportStatusHistory.query.filter_by(report_id=report_id).order_by(ReportStatusHistory.changed_at.asc()).all()
    return render_template(
        "report_detail.html", report=report, history=history, status_labels=STATUS_LABELS
    )


@bp.route("/<int:report_id>/confirm", methods=["POST"])
@login_required
def confirm_resolved(report_id):
    """Citizen confirms the repair is actually done (final step of the pipeline)."""
    report = db.session.get(Report, report_id)
    if report is None:
        abort(404)
    if report.user_id != current_user.id:
        abort(403)
    if report.status != "completed":
        flash("This report isn't marked as completed yet.", "warning")
        return redirect(url_for("reports.detail", report_id=report_id))

    report.status = "resolved_confirmed"
    
    history_entry = ReportStatusHistory(
        report_id=report_id,
        old_status='completed',
        new_status='resolved_confirmed',
        changed_by=current_user.id,
        note='Confirmed by reporting citizen'
    )
    db.session.add(history_entry)
    db.session.commit()
    flash("Thanks for confirming! Report closed.", "success")
    return redirect(url_for("reports.detail", report_id=report_id))


@bp.route("/notifications")
@login_required
def notifications():
    rows = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).limit(30).all()
    
    # Mark as read
    for row in rows:
        if not row.is_read:
            row.is_read = True
    db.session.commit()
    
    return render_template("notifications.html", notifications=rows)
