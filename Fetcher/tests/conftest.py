import pytest
from app import create_app, db
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
import time

@pytest.fixture(scope='session')
def postgres_container():
    """
    Fixture to ensure the PostgreSQL container is up and running.
    """
    import docker
    client = docker.from_env()
    container = client.containers.run(
        "postgres:13",
        name="test_postgres",
        environment={
            "POSTGRES_USER": "myuser",
            "POSTGRES_PASSWORD": "mypassword",
            "POSTGRES_DB": "test_database"
        },
        ports={"5432/tcp": 5432},
        detach=True,
    )

    # Wait for the PostgreSQL server to start
    time.sleep(10)

    yield container

    # Clean up
    container.stop()
    container.remove()

@pytest.fixture(scope='session')
def test_database(postgres_container):
    """
    Fixture to set up and tear down the test database.
    """
    test_db_url = "postgresql://myuser:mypassword@localhost:5432/test_database"
    engine = create_engine(test_db_url)
    if not database_exists(engine.url):
        create_database(engine.url)
    yield test_db_url
    drop_database(engine.url)

@pytest.fixture(scope='session')
def app(test_database):
    """
    Fixture to set up the Flask app with a test database.
    """
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": test_database,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """
    Fixture to set up a test client.
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """
    Fixture to set up a test CLI runner.
    """
    return app.test_cli_runner()
