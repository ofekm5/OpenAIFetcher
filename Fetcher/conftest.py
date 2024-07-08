import pytest
from app import create_app

class Config:
    TESTING = True
    DEBUG = True

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(Config)
    yield app

@pytest.fixture
def client(app):
    return app.test_client()
