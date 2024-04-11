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

    def test_add_face_post(self, monkeypatch):
        """
        Test the /add-face POST route.

        Args:
            monkeypatch (pytest.MonkeyPatch): A pytest fixture for monkeypatching.

        Returns:
            None: This function does not return anything.
        """

        # Define mock image data
        mocked_image_data = "data:image/jpeg;base64,mocked_base64_data"

        # Define a mock request object for POST method
        def mock_post():
            return {"image_data": mocked_image_data}

        # Apply the mock to Flask's request object
        monkeypatch.setattr("flask.request", mock_post)

        # Make a POST request to the route
        response = self.app.post("/add-face", data={"image_data": mocked_image_data})

        # Check if the response status code is 200
        assert response.status_code == 200

        # Check if the image is saved to the file
        with open("images/captured_image.jpg", "rb") as f:
            saved_image_data = f.read()

        # Decode base64 image data
        decoded_image_data = base64.b64decode(mocked_image_data.split(",")[1])

        # Assert that the saved image data matches the decoded image data
        assert saved_image_data == decoded_image_data

        # Assert that the response message indicates successful image capture
        assert b"Image captured successfully!" in response.data

    def test_request_data_and_display_result(self, mock_db):
        """
        Test the /found-faces route.

        Args:
            mock_db: Mock database fixture.
        """

        # Make request and check response
        response = self.app.get("/found-faces")
        assert response.status_code == 200

        # Check if the sample data is present in the response
        response_data_str = response.data.decode("utf-8")
        for data in mock_db.Users.find.return_value:
            assert data["name"] in response_data_str
            assert str(data["age"]) in response_data_str
