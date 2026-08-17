from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='citizen')
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    reports = db.relationship('Report', backref='reporter', lazy=True, foreign_keys='Report.user_id')
    assigned_reports = db.relationship('Report', backref='assigned_officer', lazy=True, foreign_keys='Report.assigned_officer_id')

class Report(db.Model):
    __tablename__ = 'reports'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    damage_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(20), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    address_hint = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    status = db.Column(db.String(30), nullable=False, default='new')
    priority_score = db.Column(db.Float, nullable=False, default=0.0)
    duplicate_of = db.Column(db.Integer, db.ForeignKey('reports.id'))
    duplicate_count = db.Column(db.Integer, nullable=False, default=0)
    assigned_officer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ai_suggested_type = db.Column(db.String(50))
    ai_suggested_severity = db.Column(db.String(20))
    ai_reasoning = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    status_history = db.relationship('ReportStatusHistory', backref='report', lazy=True, cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='report', lazy=True, cascade='all, delete-orphan')
    duplicates = db.relationship('Report', backref=db.backref('parent_report', remote_side=[id]), lazy='dynamic')

class ReportStatusHistory(db.Model):
    __tablename__ = 'report_status_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'), nullable=False)
    old_status = db.Column(db.String(30))
    new_status = db.Column(db.String(30), nullable=False)
    changed_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    note = db.Column(db.Text)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref='status_changes')

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('reports.id'))
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref='notifications')
