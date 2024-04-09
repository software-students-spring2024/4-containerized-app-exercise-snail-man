"""

Web-App for displayinig the data from ../machine-learning client in 
a (hopefully) Human-Readable Format

"""

import os
from flask import Flask, render_template, request
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ML_CLIENT_URL = os.getenv("ML_CLIENT_URL", "http://localhost:5001/receive_data")


@app.route("/add-face", methods=["GET", "POST"])
def add_face():
    if request.method == "POST":
        # Decode base64 image data
        image_data = request.form["image_data"]
        image_data = base64.b64decode(image_data.split(",")[1])

        # Write image to file
        with open("images/captured_image.jpg", "wb") as f:
            f.write(image_data)

        return "Image captured successfully!"

    return render_template("addFace.html")


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
    app.run()
