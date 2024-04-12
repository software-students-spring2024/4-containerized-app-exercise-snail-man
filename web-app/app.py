"""

Web-App for displayinig the data from ../machine-learning client in 
a (hopefully) Human-Readable Format

"""

import os
from hashlib import sha256
import base64
from flask import Flask, render_template, request
from dotenv import load_dotenv
import pymongo
import requests

load_dotenv()

app = Flask(__name__)

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


@app.route("/add-face", methods=["GET", "POST"])
def add_face():
    """
    Renders a video stream from the camera with a button to capture image.
    Recieves captured image and saves it
    """
    if request.method == "POST":
        # Decode base64 image data
        image_data = request.form["image_data"]
        image_data = base64.b64decode(image_data.split(",")[1])

        db.Raw.insert_one(
            {
                "imageData": image_data,
                "imageName": sha256(image_data.encode("utf-8")).hexdigest(),
            }
        )
        requests.post(
            "http:////machine-learning-client:5000/find-face",
            {"image_name": sha256(image_data.encode("utf-8")).hexdigest()},
            timeout=10,
        )
        # Write image to file
        with open("images/captured_image.jpg", "wb") as f:
            f.write(image_data)

        return "Image captured successfully!"
    return render_template("addFace.html")


@app.route("/found-faces", methods=["GET"])
def found_faces():
    """
    Displays all processed images in the database

    Returns:
        html: a list displaying all the currently stored processed images

    """
    pics = db.Processed.find()
    # Create a folder named 'images' if it doesn't exist
    if not os.path.exists("images"):
        os.makedirs("images")

    image_files = []

    # Iterate over the retrieved documents
    for i, pic in enumerate(pics):
        image_data = pic.get("image_data")

        # Save the image to the 'images' folder
        image_path = f"images/image_{i}.jpg"
        with open(image_path, "wb") as f:
            f.write(image_data)

        image_files.append(image_path)

    return render_template("foundFaces.html", image_files=image_files)


if __name__ == "__main__":
    app.run("0.0.0.0")
