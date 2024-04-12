""" Machine Learning Client for face detection """

import os
import cv2
from flask import Flask, render_template, request
from dotenv import load_dotenv
import pymongo

# Ensures that OpenCV is correctly imported
cv2 = globals()["cv2"]

load_dotenv()

cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = cxn[os.getenv("MONGO_DB")]  # store a reference to the database
print(db)

# try:
# verify the connection works by pinging the database
cxn.admin.command("ping")  # The ping command is cheap and does not require auth.
print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
# except Exception as e:
# the ping command failed, so the connection is not available.
# print(" * MongoDB connection error:", e)  # debug


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
    output_image_path = "images/detected_faces.jpg"
    cv2.imwrite(output_image_path, input_image)

    cv2.destroyAllWindows()  # Ensure all windows are closed when done
    return output_image_path


load_dotenv()

app = Flask(__name__)


@app.route("/find-face", methods=["GET"])
def test():
    """
    Checks data-base for new photos, and processes them
    """
    image_hash = request.body.get("image_name")
    image = db.Raw.find_one({"imageName": image_hash})
    image_path = f'images/image_{image["imageName"]}.jpg'
    with open(image_path, "wb") as f:
        f.write(image["image_data"])
    detect_and_display_faces(image_path)
    return render_template("result.html")


# Example usage
print(detect_and_display_faces("images/test.png"))

if __name__ == "__main__":
    app.run("0.0.0.0")
