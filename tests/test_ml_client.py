"""
Test file for machine-learning-client
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import numpy as np
import cv2

sys.path.append("machine-learning-client")
from face_detection import detect_and_display_faces

# Ensures that OpenCV is correctly imported
cv2 = globals()["cv2"]


class TestDetectAndDisplayFaces(unittest.TestCase):
    """
    Class for testing image paths whether valid or invalid
    """

    @patch("cv2.CascadeClassifier")
    @patch("cv2.imread")
    def test_with_random_image(self, mock_imread, mock_cascade_classifier):
        """
        Test the `detect_and_display_faces` function with a mock image to ensure
        it correctly processes an image and returns the expected file path.

        This method simulates reading an image file by using a mock object
        (`mock_imread`) for the image reading function.
        It creates a fake image, a 100x100 pixel RGB image
        with all pixels set to black, and configures `mock_imread`

        Parameters:
        - mock_imread (MagicMock): A mock object to replace `imread` function
                                    in the `detect_and_display_faces`
                                    function, allowing control over its
                                    output without reading a real file.

        Assertions:
        - Ensures that the output path of `detect_and_display_faces` matches
        'images/detected_faces.jpg',
        confirming that the function processes the mock image
        correctly and outputs the expected result.

        Returns:
        - None
        """
        mock_imread.return_value = cv2.imread("images/test.jpg")
        # Create a fake image array
        fake_image = np.zeros((100, 100, 3), dtype=np.uint8)
        # Set the return value of the mock to this fake image
        mock_imread.return_value = fake_image
        # Mock the CascadeClassifier and its detectMultiScale method
        mock_classifier_instance = MagicMock()
        # Simulate a detected face
        mock_classifier_instance.detectMultiScale.return_value = [(1, 2, 3, 4)]
        mock_cascade_classifier.return_value = mock_classifier_instance

        # Call the function
        result_path = detect_and_display_faces("../images/test.png")
        # Asserts
        self.assertEqual(result_path, "images/detected_faces.jpg")

    @patch("cv2.imread")
    @patch("cv2.imwrite")
    def test_invalid_image_path(self, mock_imwrite, mock_imread):
        """
        Test the `detect_and_display_faces` function's handling of an invalid image path
        by ensuring it raises a FileNotFoundError and does not attempt to save an output image.

        Parameters:
        - mock_imwrite (MagicMock): Mock of the `cv2.imwrite`
            function to verify no image gets saved.
        - mock_imread (MagicMock): Mock of the `cv2.imread` function,
            set to return `None` to simulate an error in file reading.

        Assertions:
        - Asserts that a FileNotFoundError is raised when `
            detect_and_display_faces` is called with an invalid image path.
        - Ensures that `mock_imwrite` is not called, confirming
            that no output file is attempted to be saved when the input is invalid.

        Returns:
        - None
        """
        # Mock the imread function to return None, simulating an invalid image path
        mock_imread.return_value = None

        with self.assertRaises(FileNotFoundError):
            detect_and_display_faces("invalid_path.jpg")

        mock_imwrite.assert_not_called()  # Ensure the image is not saved


if __name__ == "__main__":
    unittest.main()
