from flask import Blueprint, jsonify, request, session

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
    Returns active (non-duplicate) reports near-ish the requested bounding box
    for the Leaflet map. Falls back to all active reports if no bbox is given.
    Resolved reports are included but marked green so users can see recent fixes.
    """
    rows = query(
        """SELECT id, damage_type, severity, status, latitude, longitude,
                  address_hint, duplicate_count, created_at
           FROM reports
           WHERE duplicate_of IS NULL
           ORDER BY created_at DESC
           LIMIT 500"""
    )

    features = []
    for r in rows:
        if r["status"] == "resolved_confirmed":
            color = "#2a9d8f"  # green
        else:
            color = MARKER_COLORS.get(r["severity"], "#e9c46a")

        features.append(
            {
                "id": r["id"],
                "lat": r["latitude"],
                "lng": r["longitude"],
                "damage_type": r["damage_type"],
                "severity": r["severity"],
                "status": r["status"],
                "address_hint": r["address_hint"],
                "duplicate_count": r["duplicate_count"],
                "color": color,
                "created_at": r["created_at"],
            }
        )

    return jsonify(features)


@bp.route("/reports/<int:report_id>/status")
@login_required
def report_status(report_id):
    """Lightweight polling endpoint a report-detail page can hit every N seconds
    to reflect status changes without a full page reload (simulates real-time
    updates without requiring a websocket server)."""
    report = query("SELECT status, updated_at FROM reports WHERE id = ?", (report_id,), one=True)
    if report is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"status": report["status"], "updated_at": report["updated_at"]})


@bp.route("/notifications/unread_count")
@login_required
def unread_count():
    row = query(
        "SELECT COUNT(*) c FROM notifications WHERE user_id = ? AND is_read = 0",
        (session["user_id"],),
        one=True,
    )
    return jsonify({"count": row["c"]})
