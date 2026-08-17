from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from werkzeug.security import generate_password_hash

from models.db import query, execute
from utils.decorators import roles_required
from services.priority import recalculate_priority

bp = Blueprint("admin", __name__, url_prefix="/admin")

# Valid forward transitions in the pipeline:
#   New -> Verification -> Priority Calculation -> Assign Officer
#        -> Under Repair -> Completed -> User Verification
NEXT_STATUS = {
    "new": "verified",
    "verified": "assigned",
    "assigned": "under_repair",
    "under_repair": "completed",
}


@bp.route("/")
@roles_required("admin", "officer")
def dashboard():
    stats = {
        "total": query("SELECT COUNT(*) c FROM reports WHERE duplicate_of IS NULL", one=True)["c"],
        "new": query("SELECT COUNT(*) c FROM reports WHERE status='new' AND duplicate_of IS NULL", one=True)["c"],
        "pending": query(
            "SELECT COUNT(*) c FROM reports WHERE status IN ('verified','assigned','under_repair') AND duplicate_of IS NULL",
            one=True,
        )["c"],
        "completed": query(
            "SELECT COUNT(*) c FROM reports WHERE status IN ('completed','resolved_confirmed') AND duplicate_of IS NULL",
            one=True,
        )["c"],
        "critical": query(
            "SELECT COUNT(*) c FROM reports WHERE severity='critical' AND status NOT IN ('resolved_confirmed','rejected') AND duplicate_of IS NULL",
            one=True,
        )["c"],
    }

    avg_repair_row = query(
        """SELECT AVG(julianday(updated_at) - julianday(created_at)) AS avg_days
           FROM reports
           WHERE status IN ('completed', 'resolved_confirmed') AND duplicate_of IS NULL""",
        one=True,
    )
    stats["avg_repair_days"] = round(avg_repair_row["avg_days"], 1) if avg_repair_row["avg_days"] else 0

    area_stats = query(
        """SELECT COALESCE(NULLIF(address_hint, ''), 'Unspecified area') AS area, COUNT(*) c
           FROM reports WHERE duplicate_of IS NULL
           GROUP BY area ORDER BY c DESC LIMIT 8"""
    )

    recent = query(
        """SELECT r.*, u.full_name AS reporter_name FROM reports r
           JOIN users u ON u.id = r.user_id
           WHERE r.duplicate_of IS NULL
           ORDER BY r.priority_score DESC, r.created_at DESC LIMIT 20"""
    )

    return render_template("admin_dashboard.html", stats=stats, area_stats=area_stats, reports=recent)


@bp.route("/reports")
@roles_required("admin", "officer")
def report_list():
    status_filter = request.args.get("status", "")
    if status_filter:
        rows = query(
            """SELECT r.*, u.full_name AS reporter_name FROM reports r
               JOIN users u ON u.id = r.user_id
               WHERE r.status = ? AND r.duplicate_of IS NULL
               ORDER BY r.priority_score DESC""",
            (status_filter,),
        )
    else:
        rows = query(
            """SELECT r.*, u.full_name AS reporter_name FROM reports r
               JOIN users u ON u.id = r.user_id
               WHERE r.duplicate_of IS NULL
               ORDER BY r.priority_score DESC"""
        )
    officers = query("SELECT id, full_name FROM users WHERE role = 'officer'")
    return render_template(
        "admin_reports.html", reports=rows, status_filter=status_filter, officers=officers
    )


@bp.route("/reports/<int:report_id>/advance", methods=["POST"])
@roles_required("admin", "officer")
def advance_status(report_id):
    report = query("SELECT * FROM reports WHERE id = ?", (report_id,), one=True)
    if report is None:
        abort(404)

    current_status = report["status"]
    next_status = NEXT_STATUS.get(current_status)
    if next_status is None:
        flash("This report has no further automatic step (it may already be completed).", "warning")
        return redirect(url_for("admin.report_list"))

    officer_id = request.form.get("officer_id")
    params = {"status": next_status}

    if next_status == "assigned":
        if not officer_id:
            flash("Select an officer to assign before advancing this report.", "danger")
            return redirect(url_for("admin.report_list"))
        execute(
            "UPDATE reports SET assigned_officer_id = ?, status = ?, updated_at = datetime('now') WHERE id = ?",
            (officer_id, next_status, report_id),
        )
    else:
        execute(
            "UPDATE reports SET status = ?, updated_at = datetime('now') WHERE id = ?",
            (next_status, report_id),
        )

    execute(
        "INSERT INTO report_status_history (report_id, old_status, new_status, changed_by) VALUES (?, ?, ?, ?)",
        (report_id, current_status, next_status, session["user_id"]),
    )

    if next_status == "verified":
        recalculate_priority(report_id)

    if next_status == "completed":
        execute(
            "INSERT INTO notifications (user_id, report_id, message) VALUES (?, ?, ?)",
            (report["user_id"], report_id, "Your reported issue has been marked as repaired. Please confirm."),
        )

    flash(f"Report #{report_id} moved to '{next_status.replace('_', ' ')}'.", "success")
    return redirect(url_for("admin.report_list"))


@bp.route("/reports/<int:report_id>/reject", methods=["POST"])
@roles_required("admin", "officer")
def reject_report(report_id):
    report = query("SELECT * FROM reports WHERE id = ?", (report_id,), one=True)
    if report is None:
        abort(404)
    reason = request.form.get("reason", "").strip()
    execute(
        "UPDATE reports SET status = 'rejected', updated_at = datetime('now') WHERE id = ?",
        (report_id,),
    )
    execute(
        "INSERT INTO report_status_history (report_id, old_status, new_status, changed_by, note) VALUES (?, ?, 'rejected', ?, ?)",
        (report_id, report["status"], session["user_id"], reason),
    )
    execute(
        "INSERT INTO notifications (user_id, report_id, message) VALUES (?, ?, ?)",
        (report["user_id"], report_id, f"Your report was rejected. Reason: {reason or 'not specified'}"),
    )
    flash(f"Report #{report_id} rejected.", "info")
    return redirect(url_for("admin.report_list"))


@bp.route("/staff")
@roles_required("admin")
def manage_staff():
    # Only admins can see this page
    staff_members = query(
        "SELECT id, full_name, email, role, created_at FROM users WHERE role IN ('admin', 'officer') ORDER BY role, created_at DESC"
    )
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

    existing = query("SELECT id FROM users WHERE email = ?", (email,), one=True)
    if existing:
        flash("An account with that email already exists.", "danger")
        return redirect(url_for("admin.manage_staff"))

    # Create new officer
    pwd_hash = generate_password_hash(password)
    execute(
        "INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, 'officer')",
        (full_name, email, pwd_hash)
    )
    flash(f"Officer account for {full_name} created successfully!", "success")
    return redirect(url_for("admin.manage_staff"))
