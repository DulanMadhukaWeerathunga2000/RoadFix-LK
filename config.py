import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", os.path.join(BASE_DIR, "database", "roadfix.db")
    )
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "images", "reports")
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp"}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024  # 8 MB max upload

    # Duplicate-detection radius, in meters
    DUPLICATE_RADIUS_METERS = 50

    # Priority scoring weights
    SEVERITY_WEIGHTS = {"low": 1, "medium": 2, "high": 3, "critical": 4}
