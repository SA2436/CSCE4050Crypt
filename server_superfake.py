#Task 2.7 This will be the super fake server for client to GET the weather info
from flask import Flask, jsonify #Creates REST server
#using flask, install flask before running
import base64

app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def weather():
    #Reading from the response.bin to getting weather data
    with open("response.bin", "rb") as f:
        data = f.read()

    # Correct slicing with the help from ChatGPT
    nonce = data[:8]              # CTR nonce is 8 bytes
    tag = data[8:40]             # 32 bytes HMAC-SHA256
    ciphertext = data[40:]

    return jsonify({
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    })
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5028)  # Add with Stephen Alonso's last two Student ID # digits 