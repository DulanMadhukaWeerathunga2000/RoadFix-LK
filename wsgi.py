"""
WSGI entrypoint for production servers (gunicorn, uWSGI, etc.) that expect a
module-level `app` object rather than calling a factory function themselves.

Used like:  gunicorn wsgi:app
"""
from app import create_app

app = create_app()
