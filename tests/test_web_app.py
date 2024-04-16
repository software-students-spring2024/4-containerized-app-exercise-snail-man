"""
Test file for web-app/app.py    
"""

import sys
import pytest

sys.path.append("web-app")
from app import app


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
    Class for testing web app
    """

    def setup_method(self):
        """Set up the test client for each test."""
        app.testing = True
        self.app = app.test_client()

    def test_add_face_get(self):
        """Test the /add-face GET route."""
        response = self.app.get("/add-face")
        assert response.status_code == 200

    def test_add_face_get_renders_correct_template(self):
        """Test that the /add-face GET route renders the correct HTML template."""
        with self.app as client:
            response = client.get("/add-face")
            # This checks if the right template was indeed used.
            assert "Face Recognition" in response.get_data(as_text=True)
            assert response.status_code == 200

    def test_add_face_post_invalid_data(self):
        """
        Test the /add-face POST route with invalid image data.
        """
        response = self.app.post("/add-face", data={"image_data": "invalid_base64"})
        assert response.status_code == 200
        assert b"Error: Invalid image data format." in response.data
