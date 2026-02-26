#This will be the server for client to GET the weather info
from flask import Flask, jsonify
#using flask, install flask before running

app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def weather():
    data = {
        "location": "Denton, TX",
        "temperature_c": 10,
        "temperature_f": 50,
        "condition": "Partly Cloudy",
        "humidity_percent": XY  # Replace XY with last two digits of Student ID
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5010)  # Replace XY with Stephen Alonso's Student ID
