import pytest
from flask.testing import FlaskClient
from unittest.mock import patch

@pytest.fixture(autouse=True, scope="session")
def mock_google_cloud_storage():
    """This function will ensure that unit tests 
    do not try to connect to Google Cloud Storage 
    during execution"""
    with patch('google.cloud.storage.Client') as mock_client:
        yield mock_client

from src.app import app

@pytest.fixture(autouse=True, scope="session")
def fake_client() -> FlaskClient:
    """This function creates a test client that
    can be used to make requests to the app.

    Returns:
    - TestClient: A test client to simulate requests
    to the app."""
    return app.test_client()
