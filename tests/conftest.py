import pytest
from flask.testing import FlaskClient

from src.app import app


@pytest.fixture(autouse=True, scope="session")
def fake_client() -> FlaskClient:
    """This function creates a test client that
    can be used to make requests to the app.

    Returns:
    - TestClient: A test client to simulate requests
    to the app."""

    return FlaskClient(app)
