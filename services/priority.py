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
from models.models import db, Report


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
    report = db.session.get(Report, report_id)
    if report is None:
        return
    
    # report.created_at is already a datetime object in SQLAlchemy
    created_at_dt = report.created_at
    age_days = max((datetime.utcnow() - created_at_dt).days, 0)
    
    weights = current_app.config["SEVERITY_WEIGHTS"]
    severity_component = weights.get(report.severity, 1) * 10
    duplicate_component = report.duplicate_count * 5
    age_component = age_days * 0.5
    
    score = round(severity_component + duplicate_component + age_component, 2)
    
    report.priority_score = score
    db.session.commit()
    return score
