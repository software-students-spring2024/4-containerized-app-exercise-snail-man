"""

Web-App for displayinig the data from ../machine-learning client in 
a (hopefully) Human-Readable Format

"""

import os
import base64
from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ML_CLIENT_URL = os.getenv("ML_CLIENT_URL", "http://localhost:5001/receive_data")


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

        # Write image to file
        with open("images/captured_image.jpg", "wb") as f:
            f.write(image_data)

        return "Image captured successfully!"
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

#    db.Users.insert_one({"imageData": image_data,
#                            "imageName": sha256(image_data.encode('utf-8')).hexdigest()})
#    fetch('http:////machine-learning-client:5000/find-face', {
#            method: 'POST',
#            body: 'image_data=' + sha256(image_data.encode('utf-8')).hexdigest(),
#        })


@app.route("/display-data", methods=["GET"])
def request_data_and_display_result():
    """
    Gets JSON of data from API Endpont ML_CLENT_URL and renders it in result.html

    Returns:
        html: Table displaying data

    """
    data_to_send = {"data": "Your data to be analyzed"}

    response = requests.post(ML_CLIENT_URL, json=data_to_send, timeout=10)

    analysis_result = response.json()

    return render_template("result.html", analysis_result=analysis_result)


if __name__ == "__main__":
    app.run("0.0.0.0")
