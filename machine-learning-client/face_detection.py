""" Machine Learning Client for face detection """

import cv2

# Ensures that OpenCV is correctly imported
cv2 = globals()["cv2"]


def detect_and_display_faces(image_path):
    """
    Detects faces in an image, draws rectangles around them, and saves the result.

    This function loads a specified image, 
    detects faces using OpenCV's Haar feature-based cascade classifiers,
    draws rectangles around detected faces, 
    and saves the image with detections to the current directory.

    Parameters:
    - image_path: A string representing the path to the input image file.

    The function saves the output image with rectangles 
    in the current directory named 'detected_faces.jpg'.

    Returns:
    - output image path.
    """
    # Load the face detection model
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    # Read the input image
    input_image = cv2.imread(image_path)

    # Convert the image to grayscale for the face detection algorithm
    grayscale_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)

    # Detect faces within the image
    # Chose a high minNeighbors value to reduce false positives
    faces = face_cascade.detectMultiScale(
        grayscale_image, scaleFactor=1.1, minNeighbors=7
    )
    # Draw rectangles around detected faces
    for x, y, width, height in faces:
        cv2.rectangle(input_image, (x, y), (x + width, y + height), (0, 0, 255), 2)

    # Save the result in the current directory
    output_image_path = "detected_faces.jpg"
    cv2.imwrite(output_image_path, input_image)

    cv2.destroyAllWindows()  # Ensure all windows are closed when done
    return output_image_path


# Example usage
#detect_and_display_faces("test.png")
