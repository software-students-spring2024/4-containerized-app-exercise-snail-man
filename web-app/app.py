"""

Web-App for displayinig the data from ../machine-learning client in 
a (hopefully) Human-Readable Format

"""

import os
import base64
from flask import Flask, render_template, request
import pymongo

# import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ML_CLIENT_URL = os.getenv("ML_CLIENT_URL", "http://localhost:5001/receive_data")


mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
mongo_db = os.getenv("MONGO_DB", "default_database")

mongo_client = pymongo.MongoClient(mongo_uri)
db = mongo_client[mongo_db]


@app.route("/add-face", methods=["GET", "POST"])
def add_face():
    """
    Renders a video stream from the camera with a button to capture image.
    Recieves captured image and saves it
    """
    if request.method == "POST":
        # Decode base64 image data
        try:
            image_data = request.form["image_data"]
            image_data = base64.b64decode(image_data.split(",")[1])
        except IndexError:
            return "Error: Invalid image data format."

        # Write image to file
        try:
            with open("images/captured_image.jpg", "wb") as f:
                f.write(image_data)
            return "Image captured successfully!"
        except IOError as e:
            return f"Error saving image: {e}"

    return render_template("addFace.html")


# code to eventually send image to database and query ML
# from flask_pymongo import PyMongo
# from pymongo.mongo_client import MongoClient
# from pymongo.server_api import ServerApi
# from hashlib import sha256
# import pymongo

# cxn = pymongo.MongoClient(os.getenv("MONGO_URI"))
# db = cxn[os.getenv("MONGO_DB")]  # store a reference to the database
# print(db)

# try:
# verify the connection works by pinging the database
# cxn.admin.command("ping")  # The ping command is cheap and does not require auth.
# print(" *", "Connected to MongoDB!")  # if we get here, the connection worked!
#    except Exception as e:
# the ping command failed, so the connection is not available.
# print(" * MongoDB connection error:", e)  # debug

#    db.Raw.insert_one({"imageData": image_data,
#                            "imageName": sha256(image_data.encode('utf-8')).hexdigest()})
#    fetch('http:////machine-learning-client:5000/find-face', {
#            method: 'POST',
#            body: 'image_data=' + sha256(image_data.encode('utf-8')).hexdigest(),
#        })


@app.route("/found-faces", methods=["GET"])
def found_faces():
    """
    Displays all processed images in the database

    Returns:
        html: a list displaying all the currently stored processed images

    """
    data_from_mongo = list(db.Users.find())

    keys = data_from_mongo[0].keys() if data_from_mongo else []

    # pics = db.Processed.find()
    # Create a folder named 'images' if it doesn't exist
    # if not os.path.exists('images'):
    # os.makedirs('images')

    # image_files = []

    # Iterate over the retrieved documents
    # for i, pic in enumerate(pics):
    # image_data = pic.get('image_data')

    # Save the image to the 'images' folder
    # image_path = f'images/image_{i}.jpg'
    # with open(image_path, 'wb') as f:
    # f.write(image_data)

    # image_files.append(image_path)

    # return render_template('foundFaces.html', image_files=image_files) changed for template's sake
    return render_template("result.html", analysis_result=data_from_mongo, keys=keys)


if __name__ == "__main__":
    app.run("0.0.0.0")
