from flask import Blueprint, jsonify, session
from models.db import query
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

    rows = query(
        """
        SELECT
            id,
            damage_type,
            severity,
            status,
            latitude,
            longitude,
            address_hint,
            duplicate_count,
            created_at
        FROM reports
        WHERE duplicate_of IS NULL
        ORDER BY created_at DESC
        LIMIT 500
        """
    )

    features = []

    for r in rows:

        # Ignore invalid GPS coordinates
        if r["latitude"] is None or r["longitude"] is None:
            continue

        try:
            latitude = float(r["latitude"])
            longitude = float(r["longitude"])
        except (TypeError, ValueError):
            continue

        # Ignore impossible coordinates
        if not (-90 <= latitude <= 90):
            continue

        if not (-180 <= longitude <= 180):
            continue

        # Resolved = green
        if r["status"] == "resolved_confirmed":
            color = "#2a9d8f"
        else:
            color = MARKER_COLORS.get(
                r["severity"],
                "#e9c46a"
            )

        features.append(
            {
                "id": r["id"],
                "lat": latitude,
                "lng": longitude,
                "damage_type": r["damage_type"],
                "severity": r["severity"],
                "status": r["status"],
                "address_hint": r["address_hint"],
                "duplicate_count": r["duplicate_count"] or 0,
                "created_at": r["created_at"],
                "color": color,
            }
        )

    return jsonify(features)


@bp.route("/reports/<int:report_id>/status")
@login_required
def report_status(report_id):

    report = query(
        """
        SELECT status, updated_at
        FROM reports
        WHERE id = ?
        """,
        (report_id,),
        one=True,
    )

    if report is None:
        return jsonify({
            "error": "Report not found"
        }), 404

    return jsonify({
        "status": report["status"],
        "updated_at": report["updated_at"]
    })


@bp.route("/notifications/unread_count")
@login_required
def unread_count():

    row = query(
        """
        SELECT COUNT(*) AS count
        FROM notifications
        WHERE user_id = ?
        AND is_read = 0
        """,
        (session["user_id"],),
        one=True,
    )

    return jsonify({
        "count": row["count"]
    })