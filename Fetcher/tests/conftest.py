# conftest.py
import pytest
from app import create_app
from app.database import db

@pytest.fixture(scope='session')
def app():
    app = create_app()
    with app.app_context():
        import time
        retries = 5
        while retries > 0:
            try:
                db.create_all()
                break
            except Exception as e:
                print(f"Database connection failed: {e}")
                time.sleep(5)
                retries -= 1

        if retries == 0:
            raise Exception("Database connection failed after several retries")
        
        yield app

@pytest.fixture
def client(app):
    return app.test_client()
