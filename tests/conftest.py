import os
import tempfile
import pytest
from app import create_app
from models.db import init_db

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    
    # Configure the app for testing
    class TestConfig:
        TESTING = True
        DATABASE_PATH = db_path
        SECRET_KEY = 'test_secret'
        UPLOAD_FOLDER = tempfile.mkdtemp()
        WTF_CSRF_ENABLED = False
        
    app = create_app(TestConfig)
    
    with app.app_context():
        init_db(app)

    yield app

    # Clean up after tests
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
