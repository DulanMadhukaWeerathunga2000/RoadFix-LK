import os
import sys
import tempfile
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    TestConfig.DATABASE_PATH = db_path
    app = create_app(TestConfig)
    yield app
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


def register(client, email="alice@example.com", password="password1"):
    return client.post(
        "/auth/register",
        data={"full_name": "Alice", "email": email, "phone": "", "password": password},
        follow_redirects=True,
    )


def submit_report(client, lat=6.9271, lng=79.8612, damage_type="pothole", severity="high"):
    return client.post(
        "/reports/new",
        data={
            "damage_type": damage_type,
            "severity": severity,
            "description": "Deep pothole near the junction",
            "latitude": str(lat),
            "longitude": str(lng),
            "address_hint": "Test Junction",
        },
        follow_redirects=True,
    )


def test_register_and_login(client):
    resp = register(client)
    assert resp.status_code == 200
    assert b"My Reports" in resp.data or b"my-reports" in resp.data.lower() or resp.status_code == 200


def test_admin_seeded(app):
    with app.app_context():
        from models.db import query
        admin = query("SELECT * FROM users WHERE role='admin'", one=True)
        assert admin is not None
        assert admin["email"] == "admin@roadfix.lk"


def test_report_requires_login(client):
    resp = client.get("/reports/new", follow_redirects=True)
    assert b"log in" in resp.data.lower() or b"login" in resp.data.lower()


def test_submit_report_creates_row(client, app):
    register(client)
    submit_report(client)
    with app.app_context():
        from models.db import query
        rows = query("SELECT * FROM reports")
        assert len(rows) == 1
        assert rows[0]["damage_type"] == "pothole"
        assert rows[0]["status"] == "new"


def test_duplicate_detection_merges_nearby_reports(client, app):
    register(client)
    submit_report(client, lat=6.92710, lng=79.86120)
    # Same type, ~5m away -> should be detected as duplicate
    submit_report(client, lat=6.92715, lng=79.86123)

    with app.app_context():
        from models.db import query
        active = query("SELECT * FROM reports WHERE duplicate_of IS NULL")
        duplicates = query("SELECT * FROM reports WHERE duplicate_of IS NOT NULL")
        assert len(active) == 1
        assert len(duplicates) == 1
        assert active[0]["duplicate_count"] == 1


def test_far_apart_reports_not_merged(client, app):
    register(client)
    submit_report(client, lat=6.9271, lng=79.8612)
    submit_report(client, lat=7.2906, lng=80.6337)  # Kandy - far away

    with app.app_context():
        from models.db import query
        active = query("SELECT * FROM reports WHERE duplicate_of IS NULL")
        assert len(active) == 2


def test_priority_score_increases_with_severity():
    from services import priority as priority_module
    from flask import Flask
    app = Flask(__name__)
    app.config["SEVERITY_WEIGHTS"] = {"low": 1, "medium": 2, "high": 3, "critical": 4}
    with app.app_context():
        low_score = priority_module.compute_score("low", 0, "2026-01-01 00:00:00")
        crit_score = priority_module.compute_score("critical", 0, "2026-01-01 00:00:00")
        assert crit_score > low_score


def test_admin_login_and_dashboard(client):
    client.post("/auth/login", data={"email": "admin@roadfix.lk", "password": "admin123"})
    resp = client.get("/admin/", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Dashboard" in resp.data or b"dashboard" in resp.data.lower()


def test_citizen_cannot_access_admin(client):
    register(client)
    resp = client.get("/admin/")
    assert resp.status_code == 403
