"""
Lightweight data-access layer for RoadFix LK.

We use Python's built-in sqlite3 module directly (row_factory = sqlite3.Row)
instead of an ORM, so the project has zero third-party runtime dependencies
beyond Flask. Swapping SQLITE_PATH for a PostgreSQL DSN + psycopg2 later
would only require changes inside this module.
"""
import sqlite3
import os
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE_PATH"],
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    os.makedirs(os.path.dirname(app.config["DATABASE_PATH"]), exist_ok=True)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    schema_path = os.path.join(os.path.dirname(__file__), "..", "database", "schema.sql")
    with app.app_context():
        db = get_db()
        with open(schema_path, "r") as f:
            db.executescript(f.read())
        db.commit()
        _seed_admin(db)
    app.teardown_appcontext(close_db)


def _seed_admin(db):
    """Create a default admin account on first run so the admin side is reachable."""
    from werkzeug.security import generate_password_hash

    existing = db.execute("SELECT id FROM users WHERE role = 'admin' LIMIT 1").fetchone()
    if existing is None:
        db.execute(
            "INSERT INTO users (full_name, email, password_hash, role) VALUES (?, ?, ?, ?)",
            ("Admin", "admin@roadfix.lk", generate_password_hash("admin123"), "admin"),
        )
        db.commit()


def query(sql, args=(), one=False):
    db = get_db()
    cur = db.execute(sql, args)
    rows = cur.fetchall()
    return (rows[0] if rows else None) if one else rows


def execute(sql, args=()):
    db = get_db()
    cur = db.execute(sql, args)
    db.commit()
    return cur.lastrowid
