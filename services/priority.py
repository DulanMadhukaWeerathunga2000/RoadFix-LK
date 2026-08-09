"""
Priority Calculation
--------------------
priority_score = severity_weight * 10
                + duplicate_count * 5      (more citizens affected -> higher priority)
                + age_days * 0.5           (older unresolved reports rise over time)

Higher score = more urgent. This feeds the "Priority Calculation" stage of the
admin pipeline (New -> Verification -> Priority Calculation -> Assign Officer -> ...).
"""
from datetime import datetime
from flask import current_app
from models.db import query, execute


def compute_score(severity, duplicate_count, created_at):
    weights = current_app.config["SEVERITY_WEIGHTS"]
    severity_component = weights.get(severity, 1) * 10
    duplicate_component = duplicate_count * 5

    try:
        created = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        age_days = max((datetime.utcnow() - created).days, 0)
    except (ValueError, TypeError):
        age_days = 0

    age_component = age_days * 0.5
    return round(severity_component + duplicate_component + age_component, 2)


def recalculate_priority(report_id):
    report = query("SELECT * FROM reports WHERE id = ?", (report_id,), one=True)
    if report is None:
        return
    score = compute_score(report["severity"], report["duplicate_count"], report["created_at"])
    execute("UPDATE reports SET priority_score = ? WHERE id = ?", (score, report_id))
    return score
