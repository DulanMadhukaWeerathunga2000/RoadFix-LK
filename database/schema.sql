-- RoadFix LK Database Schema (SQLite)
-- This file documents the schema. It is applied automatically by models/db.py:init_db()

CREATE TABLE IF NOT EXISTS users (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name       TEXT NOT NULL,
    email           TEXT NOT NULL UNIQUE,
    password_hash   TEXT NOT NULL,
    role            TEXT NOT NULL DEFAULT 'citizen',  -- citizen | officer | admin
    phone           TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS reports (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id          INTEGER NOT NULL REFERENCES users(id),
    damage_type      TEXT NOT NULL,   -- pothole | crack | sign | road_damage | streetlight
    description      TEXT,
    severity         TEXT NOT NULL,   -- low | medium | high | critical
    latitude         REAL NOT NULL,
    longitude         REAL NOT NULL,
    address_hint     TEXT,
    image_path       TEXT,
    status           TEXT NOT NULL DEFAULT 'new',
        -- new | verified | assigned | under_repair | completed | resolved_confirmed | rejected
    priority_score   REAL NOT NULL DEFAULT 0,
    duplicate_of     INTEGER REFERENCES reports(id),   -- set if merged into another report
    duplicate_count  INTEGER NOT NULL DEFAULT 0,       -- how many reports merged into this one
    assigned_officer_id INTEGER REFERENCES users(id),
    ai_suggested_type     TEXT,
    ai_suggested_severity TEXT,
    created_at       TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at       TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS report_status_history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    report_id   INTEGER NOT NULL REFERENCES reports(id),
    old_status  TEXT,
    new_status  TEXT NOT NULL,
    changed_by  INTEGER REFERENCES users(id),
    note        TEXT,
    changed_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS notifications (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL REFERENCES users(id),
    report_id   INTEGER REFERENCES reports(id),
    message     TEXT NOT NULL,
    is_read     INTEGER NOT NULL DEFAULT 0,
    created_at  TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_reports_status ON reports(status);
CREATE INDEX IF NOT EXISTS idx_reports_location ON reports(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_reports_user ON reports(user_id);
