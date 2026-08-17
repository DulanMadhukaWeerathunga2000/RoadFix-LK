from flask_migrate import Migrate
from models.models import db

migrate = Migrate()

def init_db(app):
    db.init_app(app)
    migrate.init_app(app, db)
    # We no longer execute schema.sql automatically.
    # Flask-Migrate handles DB creation and migrations.
