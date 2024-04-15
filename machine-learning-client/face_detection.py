""" Machine Learning Client for face detection """

import os
import cv2
from flask import Flask, render_template, request
from dotenv import load_dotenv
import pymongo

# Ensures that OpenCV is correctly imported
cv2 = globals()["cv2"]

load_dotenv()

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
mongo_db = os.getenv("MONGO_DB", "default_database")

mongo_client = pymongo.MongoClient(mongo_uri)
db = mongo_client[mongo_db]


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

    print("Image Type " + image_path + str(type(input_image)))
    # If image was not loaded correctly, raise exception
    if input_image is None:
        raise FileNotFoundError(f"No file found at the specified path: {image_path}")

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
    output_image_path = "images/detected_faces.jpg"
    cv2.imwrite(output_image_path, input_image)

    cv2.destroyAllWindows()  # Ensure all windows are closed when done
    return output_image_path


load_dotenv()

app = Flask(__name__)


@app.route("/find-face", methods=["GET", "POST"])
def find_face():
    """
    Checks data-base for new photos, and processes them
    """
    print("request recieved")
    print(request.headers.get("image_name"))
    # image_hash = request.headers.get("image_name")
    # image = db.Raw.find_one({"imageName": image_hash})
    image = db.Raw.find_one({})
    print(image)
    image_name = image["imageName"]
    image_path = f'images/image_{image["imageName"]}.jpg'
    with open(image_path, "wb") as f:
        f.write(image["imageData"])
    with open(detect_and_display_faces(image_path), "rb") as f:
        processed_image_data = f.read()
    db.Processed.insert_one({"imageName": image_name, "imageData": processed_image_data})
    db.Raw.delete_one({"imageName": image_name})
    return render_template("result.html")


# Example usage
# print(detect_and_display_faces("images/test.png"))

if __name__ == "__main__":
    app.run("0.0.0.0")
# detect_and_display_faces("../images/test.png")
