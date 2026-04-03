#Task 2.4 This will be the fake server for client to GET the weather info
from flask import Flask, jsonify #Creates REST server
#using flask, install flask before running
import json

app = Flask(__name__)


@app.route('/weather', methods=['GET'])
def weather():
    data = {
        "location": "Denton, TX",
        "temperature_c": 10,
        "temperature_f": 50,
        "condition": "Partly Cloudy",
        "humidity_percent": 29  #Add with Stephen Alonso's last two Student ID # digits + 1
    }
    #Read open tag running from an attacker
    with open("tag.txt", "r") as f:
        tag = f.read()

    return jsonify({
        "data": data, 
        "tag": tag
        }) #send JSON response to client when requested 

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5029)  # Add with Stephen Alonso's last two Student ID # digits + 1
