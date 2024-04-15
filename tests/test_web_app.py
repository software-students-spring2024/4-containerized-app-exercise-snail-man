"""
Test file for web-app/app.py    
"""

import base64
import sys
import pytest

sys.path.append("web-app")
from app import app

# from _pytest.monkeypatch import monkeypatch


@pytest.fixture
def mock_db(mocker):
    """Mock database fixture."""
    mock_db = mocker.patch("app.db")
    mock_collection = mock_db.Users

    # Sample data
    sample_data = [
        {"_id": 1, "name": "John Doe", "age": 30},
        {"_id": 2, "name": "Jane Smith", "age": 25},
    ]

    # Mocking the find method of Users collection
    mock_collection.find.return_value = sample_data

    return mock_db


class TestAppRoutes:
    """
    Class for testing routes in flask web app
    """

    def setup_method(self):
        """Set up the test client for each test."""
        app.testing = True
        self.app = app.test_client()

    def test_add_face_get(self):
        """Test the /add-face GET route."""
        response = self.app.get("/add-face")
        assert response.status_code == 200
        # assert b"video stream" in response.data
        # commented out until ml-client implemented