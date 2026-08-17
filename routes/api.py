from flask_login import current_user
from flask import Blueprint, jsonify, session
from models.models import db, Report, Notification
from utils.decorators import login_required

bp = Blueprint("api", __name__, url_prefix="/api")

MARKER_COLORS = {
    "critical": "#e63946",
    "high": "#f4a261",
    "medium": "#e9c46a",
    "low": "#e9c46a",
}


@bp.route("/map/reports")
def map_reports():
    """
    Return all non-duplicate road reports for the public map.
    """

    rows = Report.query.filter(Report.duplicate_of.is_(None)).order_by(Report.created_at.desc()).limit(500).all()

    features = []

    for r in rows:

        # Ignore invalid GPS coordinates
        if r.latitude is None or r.longitude is None:
            continue

        try:
            latitude = float(r.latitude)
            longitude = float(r.longitude)
        except (TypeError, ValueError):
            continue

        # Ignore impossible coordinates
        if not (-90 <= latitude <= 90):
            continue

        if not (-180 <= longitude <= 180):
            continue

        # Resolved = green
        if r.status == "resolved_confirmed":
            color = "#2a9d8f"
        else:
            color = MARKER_COLORS.get(
                r.severity,
                "#e9c46a"
            )

        features.append(
            {
                "id": r.id,
                "lat": latitude,
                "lng": longitude,
                "damage_type": r.damage_type,
                "severity": r.severity,
                "status": r.status,
                "address_hint": r.address_hint,
                "duplicate_count": r.duplicate_count or 0,
                "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S") if r.created_at else None,
                "color": color,
            }
        )

    return jsonify(features)


@bp.route("/reports/<int:report_id>/status")
@login_required
def report_status(report_id):

    report = db.session.get(Report, report_id)

    if report is None:
        return jsonify({
            "error": "Report not found"
        }), 404

    return jsonify({
        "status": report.status,
        "updated_at": report.updated_at.strftime("%Y-%m-%d %H:%M:%S") if report.updated_at else None
    })


@bp.route("/notifications/unread_count")
@login_required
def unread_count():

    count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()

    return jsonify({
        "count": count
    })
