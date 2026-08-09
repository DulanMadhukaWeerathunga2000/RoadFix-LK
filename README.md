# RoadFix LK — Road Damage Reporting & Management Platform

A citizen-facing platform for reporting potholes, cracks, broken signs, and
other road/street-light damage in Sri Lanka, with a full admin pipeline for
verifying, prioritizing, assigning, and resolving reports — plus a live map,
duplicate-report merging, and an optional AI-assisted damage suggestion.

## Features

**Citizens**
- Register / login
- Submit a report: GPS location (auto-detected + draggable map pin), photo,
  damage type, severity, description
- Track their own reports and get notified as status changes
- Confirm a repair is actually done (closes the loop)

**Authorities (admin / officer roles)**
- Dashboard: total / new / pending / completed / critical counts, area-wise
  breakdown, average repair time
- Pipeline: **New → Verification → Priority Calculation → Assign Officer →
  Under Repair → Completed → User Verification**
- Reject reports with a reason

**Map**
- Public Leaflet/OpenStreetMap view, color-coded by severity
  (🔴 critical, 🟠 high, 🟡 medium/low, 🟢 resolved)

**Duplicate detection**
- New reports within ~50m of an existing active report of the same damage
  type are automatically merged into it instead of creating a new pipeline
  entry — the citizen sees *"A similar issue has already been reported
  nearby."* The merged report's `duplicate_count` feeds directly into its
  priority score.

**Optional AI assist**
- Uploaded photos are analyzed with an OpenCV heuristic (edge detection +
  blob shape/size) to suggest a damage type and severity. This is always
  advisory — the citizen's own selection is what gets saved; the suggestion
  is shown to admins as a cross-check, never applied automatically.

## Tech stack

| Layer      | Choice                                    |
|------------|--------------------------------------------|
| Backend    | Python 3 + Flask (Blueprints, sessions)    |
| Database   | SQLite via the stdlib `sqlite3` module (see note below) |
| Frontend   | HTML + Bootstrap 5 + vanilla JS            |
| Maps       | Leaflet.js + OpenStreetMap tiles           |
| AI (opt.)  | OpenCV heuristic (no training data needed) |
| Deployment | Docker                                     |

> **Why SQLite instead of PostgreSQL?** The original spec called for
> PostgreSQL. This build uses SQLite so the project runs anywhere with zero
> external services — genuinely useful for a portfolio/demo. All SQL lives in
> `models/db.py` and `database/schema.sql`; swapping in PostgreSQL later is a
> matter of changing the connection layer (e.g. to `psycopg2`) and adjusting
> a few SQLite-specific functions (`datetime('now')`, `julianday()`).

> **Why no Flask-SocketIO?** Same reasoning — it's an extra service/dependency.
> "Real-time" status updates are done with lightweight polling
> (`/api/reports/<id>/status`, hit every 15s from the report-detail page).
> Swapping in SocketIO later would only touch that one endpoint.

## Project structure

```
RoadFix-LK/
├── app.py                  # Flask app factory + entrypoint
├── config.py
├── requirements.txt
├── models/
│   └── db.py                # sqlite3 connection, init_db(), query()/execute() helpers
├── routes/
│   ├── auth.py               # register / login / logout
│   ├── reports.py            # citizen report submission, tracking, confirmation
│   ├── admin.py               # dashboard, pipeline actions, rejection
│   └── api.py                 # map GeoJSON-ish feed, status polling
├── services/
│   ├── duplicate_detection.py # radius + type based duplicate merging
│   ├── priority.py            # severity + duplicates + age -> priority score
│   └── ai_suggestion.py        # optional OpenCV-based damage suggestion
├── utils/
│   ├── geo.py                  # haversine distance
│   └── decorators.py            # @login_required, @roles_required
├── templates/                   # Jinja2 + Bootstrap 5 templates
├── static/css, static/js, static/images/
├── database/schema.sql           # schema reference (auto-applied on first run)
├── tests/test_basic.py            # pytest suite (auth, submission, duplicates, RBAC)
└── Dockerfile
```

## Software engineering concepts demonstrated

OOP-ish service layer separation, MVC-style structure (routes / models / templates),
a small REST-ish JSON API, session-based authentication, role-based access control
(citizen / officer / admin), a normalized relational schema with foreign keys,
server-side input validation, exception handling (e.g. AI-assist never breaks
submission), automated tests, Docker packaging, and a status-history audit log.

## Running locally

```bash
pip install -r requirements.txt
python app.py
# -> http://localhost:5000
```

The database and an admin account are created automatically on first run:

- **Admin login:** `admin@roadfix.lk` / `admin123` (change this in production!)

To promote a citizen to `officer` so they can be assigned repairs, update
their role directly in the DB for now (no UI for this yet — see "Next steps"):

```sql
UPDATE users SET role = 'officer' WHERE email = 'someone@example.com';
```

## Running tests

```bash
pip install pytest
pytest tests/ -v
```

## Running with Docker

```bash
docker build -t roadfix-lk .
docker run -p 5000:5000 roadfix-lk
```

## Deploying from GitHub without Docker (Render.com)

Render can build and run this app directly from your GitHub repo using its
native Python runtime — no Dockerfile needed.

1. **Push this project to a new GitHub repo.**
   ```bash
   cd RoadFix-LK
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/<your-username>/roadfix-lk.git
   git push -u origin main
   ```
2. **Create a Render account** at [render.com](https://render.com) and connect your GitHub account.
3. **New → Blueprint**, pick the `roadfix-lk` repo. Render will read `render.yaml`
   automatically and configure:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn wsgi:app --bind 0.0.0.0:$PORT`
   - A `SECRET_KEY` (auto-generated)
   - A 1GB persistent disk mounted at `/var/data` for the SQLite file
4. Click **Apply**. First deploy takes a few minutes (installing OpenCV takes
   the longest). You'll get a live URL like `https://roadfix-lk.onrender.com`.

   No `render.yaml`? You can set this up manually instead: **New → Web Service**
   → pick the repo → Runtime: `Python 3` → Build command `pip install -r
   requirements.txt` → Start command `gunicorn wsgi:app --bind 0.0.0.0:$PORT`.

**Important caveat (free tier):** Render's free web services don't persist a
disk unless you attach one (the `render.yaml` above does this for the
database). Uploaded report **photos** are saved under `static/images/reports/`
in the app's own filesystem, which is *not* on that persistent disk, so
they'll be wiped on every redeploy/restart on the free plan. Fine for a demo;
for production move `UPLOAD_FOLDER` onto the mounted disk (or to S3/Cloudinary)
before relying on it.

**Alternatives:** Railway and PythonAnywhere also deploy straight from GitHub
without Docker, using the same `requirements.txt` + `gunicorn wsgi:app`
pattern (Railway) or a WSGI file pointing at `wsgi.app` (PythonAnywhere).

## Suggested next steps

- Admin UI for managing officer accounts and roles
- Email/SMS notifications (currently in-app only)
- Pagination on report lists
- Swap SQLite → PostgreSQL and polling → Flask-SocketIO for a production deployment
- Replace the OpenCV heuristic with a trained pothole-detection model if a
  labelled dataset becomes available
