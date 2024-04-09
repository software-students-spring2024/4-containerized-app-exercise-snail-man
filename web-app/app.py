from flask import Flask, jsonify, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

ML_CLIENT_URL = os.getenv('ML_CLIENT_URL', 'http://localhost:5001/receive_data')

@app.route('/display-data', methods=['GET'])
def request_data_and_display_result():

    data_to_send = {"data": "Your data to be analyzed"}
    
    response = requests.post(ML_CLIENT_URL, json=data_to_send)
    
    analysis_result = response.json()

    return render_template('result.html', analysis_result=analysis_result)

if __name__ == '__main__':
    app.run(port=5000)