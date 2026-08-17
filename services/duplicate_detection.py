"""
Duplicate Report Detection
---------------------------
When a new report comes in, we look for existing *active* reports
(not completed/rejected) of the SAME damage_type within a configurable
radius (default 50m, see config.DUPLICATE_RADIUS_METERS). If one is
found, instead of creating a brand-new independent report we:

  1. Link the new report to the existing one (duplicate_of).
  2. Bump the existing report's duplicate_count, which feeds directly
     into priority scoring (more citizens affected = higher priority).
  3. Skip creating a second row in the admin pipeline, so the officer
     dashboard shows ONE incident instead of ten near-identical ones.

This is intentionally simple (radius + type match) rather than a full
ML clustering approach, but the interface is isolated in this module
so it can be swapped for something smarter later.
"""
from flask import current_app
from models.models import db, Report
from utils.geo import haversine_meters


ACTIVE_STATUSES = ("new", "verified", "assigned", "under_repair")


def find_duplicate(latitude, longitude, damage_type):
    """Return the existing report row this new report duplicates, or None."""
    radius = current_app.config["DUPLICATE_RADIUS_METERS"]

    candidates = Report.query.filter(
        Report.damage_type == damage_type,
        Report.duplicate_of == None,
        Report.status.in_(ACTIVE_STATUSES)
    ).all()

    for candidate in candidates:
        dist = haversine_meters(latitude, longitude, candidate.latitude, candidate.longitude)
        if dist <= radius:
            return candidate
    return None


def merge_into(existing_report_id):
    """Increment the duplicate counter on the existing report and recompute its priority."""
    from services.priority import recalculate_priority

    report = db.session.get(Report, existing_report_id)
    if report:
        report.duplicate_count += 1
        db.session.commit()
        recalculate_priority(existing_report_id)
