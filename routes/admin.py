from flask_login import current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash
from sqlalchemy import func

from models.models import db, User, Report, ReportStatusHistory, Notification
from utils.decorators import roles_required
from services.priority import recalculate_priority

bp = Blueprint("admin", __name__, url_prefix="/admin")

NEXT_STATUS = {
    "new": "verified",
    "verified": "assigned",
    "assigned": "under_repair",
    "under_repair": "completed",
}

@bp.route("/")
@roles_required("admin", "officer")
def dashboard():
    base_query = Report.query.filter(Report.duplicate_of.is_(None))
    
    stats = {
        "total": base_query.count(),
        "new": base_query.filter(Report.status == 'new').count(),
        "pending": base_query.filter(Report.status.in_(['verified','assigned','under_repair'])).count(),
        "completed": base_query.filter(Report.status.in_(['completed','resolved_confirmed'])).count(),
        "critical": base_query.filter(Report.severity == 'critical', ~Report.status.in_(['resolved_confirmed','rejected'])).count(),
    }

    # Calculate average repair days in python to be DB agnostic
    completed_reports = base_query.filter(Report.status.in_(['completed', 'resolved_confirmed'])).all()
    total_days = 0
    valid_reports = 0
    for r in completed_reports:
        if r.updated_at and r.created_at:
            days = (r.updated_at - r.created_at).total_seconds() / 86400.0
            total_days += days
            valid_reports += 1
    
    stats["avg_repair_days"] = round(total_days / valid_reports, 1) if valid_reports > 0 else 0

    # Area stats
    area_counts = db.session.query(
        func.coalesce(func.nullif(Report.address_hint, ''), 'Unspecified area').label('area'),
        func.count(Report.id).label('c')
    ).filter(Report.duplicate_of.is_(None)).group_by('area').order_by(func.count(Report.id).desc()).limit(8).all()
    
    # We map it to dicts like the old SQLite rows returned
    area_stats = [{"area": row.area, "c": row.c} for row in area_counts]

    recent = base_query.order_by(Report.priority_score.desc(), Report.created_at.desc()).limit(20).all()

    return render_template("admin_dashboard.html", stats=stats, area_stats=area_stats, reports=recent)


@bp.route("/reports")
@roles_required("admin", "officer")
def report_list():
    status_filter = request.args.get("status", "")
    
    query = Report.query.filter(Report.duplicate_of.is_(None))
    if status_filter:
        query = query.filter(Report.status == status_filter)
        
    rows = query.order_by(Report.priority_score.desc()).all()
    
    officers = User.query.filter_by(role='officer').all()
    
    return render_template(
        "admin_reports.html", reports=rows, status_filter=status_filter, officers=officers
    )


@bp.route("/reports/<int:report_id>/advance", methods=["POST"])
@roles_required("admin", "officer")
def advance_status(report_id):
    report = db.session.get(Report, report_id)
    if report is None:
        abort(404)

    current_status = report.status
    next_status = NEXT_STATUS.get(current_status)
    if next_status is None:
        flash("This report has no further automatic step (it may already be completed).", "warning")
        return redirect(url_for("admin.report_list"))

    officer_id = request.form.get("officer_id")

    if next_status == "assigned":
        if not officer_id:
            flash("Select an officer to assign before advancing this report.", "danger")
            return redirect(url_for("admin.report_list"))
        report.assigned_officer_id = officer_id
        
    report.status = next_status

    history = ReportStatusHistory(
        report_id=report_id,
        old_status=current_status,
        new_status=next_status,
        changed_by=current_user.id
    )
    db.session.add(history)
    db.session.commit()

    if next_status == "verified":
        recalculate_priority(report_id)

    if next_status == "completed":
        notif = Notification(
            user_id=report.user_id,
            report_id=report_id,
            message="Your reported issue has been marked as repaired. Please confirm."
        )
        db.session.add(notif)
        db.session.commit()

    flash(f"Report #{report_id} moved to '{next_status.replace('_', ' ')}'.", "success")
    return redirect(url_for("admin.report_list"))


@bp.route("/reports/<int:report_id>/reject", methods=["POST"])
@roles_required("admin", "officer")
def reject_report(report_id):
    report = db.session.get(Report, report_id)
    if report is None:
        abort(404)
        
    reason = request.form.get("reason", "").strip()
    old_status = report.status
    report.status = 'rejected'
    
    history = ReportStatusHistory(
        report_id=report_id,
        old_status=old_status,
        new_status='rejected',
        changed_by=current_user.id,
        note=reason
    )
    db.session.add(history)
    
    notif = Notification(
        user_id=report.user_id,
        report_id=report_id,
        message=f"Your report was rejected. Reason: {reason or 'not specified'}"
    )
    db.session.add(notif)
    db.session.commit()
    
    flash(f"Report #{report_id} rejected.", "info")
    return redirect(url_for("admin.report_list"))


@bp.route("/staff")
@roles_required("admin")
def manage_staff():
    # Only admins can see this page
    staff_members = User.query.filter(User.role.in_(['admin', 'officer'])).order_by(User.role, User.created_at.desc()).all()
    return render_template("admin_staff.html", staff=staff_members)


@bp.route("/staff/add", methods=["POST"])
@roles_required("admin")
def add_staff():
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not full_name or not email or len(password) < 6:
        flash("Invalid input. Please check the fields and try again.", "danger")
        return redirect(url_for("admin.manage_staff"))

    existing = User.query.filter_by(email=email).first()
    if existing:
        flash("An account with that email already exists.", "danger")
        return redirect(url_for("admin.manage_staff"))

    # Create new officer
    pwd_hash = generate_password_hash(password)
    new_user = User(
        full_name=full_name,
        email=email,
        password_hash=pwd_hash,
        role='officer'
    )
    db.session.add(new_user)
    db.session.commit()
    
    flash(f"Officer account for {full_name} created successfully!", "success")
    return redirect(url_for("admin.manage_staff"))
