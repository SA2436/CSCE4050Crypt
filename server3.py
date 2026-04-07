from flask import Flask, request, jsonify # TASK 3 Flask for REST API
from Crypto.PublicKey import RSA # RSA tools
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES # AES + crypto tools
import base64, json
import hmac, hashlib

app = Flask(__name__)

#Global variable to store shared AES key
shared_key = None

#MAC key hardcoded from task 2 
mac_key = b'cadc3239e73e53622d0664dff2651767f618a438f00ede9a6541fb1cb4835b05'

#Receive encrypted AES key
@app.route('/key', methods=['POST'])
def receive_key():
    global shared_key

    # Get encrypted key from client
    data = request.get_json()
    encoded_key = data['key']

    # Decode from Base64
    encrypted_key = base64.b64decode(encoded_key)

    # Load RSA secret key from 
    with open("secret.key", "rb") as f:
        private_key = RSA.import_key(f.read())

    # Create RSA cipher
    rsa_cipher = PKCS1_OAEP.new(private_key)

    #Decrypt AES key
    shared_key = rsa_cipher.decrypt(encrypted_key)

    print("AES key received and decrypted!")

    return "Key received successfully"


#Weather endpoint uses shared_key this task
@app.route('/weather', methods=['GET'])
def weather():
    global shared_key

    #Make sure key exchange happened
    if shared_key is None:
        return "No key established!", 400
    #Weather data for key exchange to client request
    data = {
        "location": "Denton, TX",
        "temperature_c": 10,
        "temperature_f": 50,
        "condition": "Partly Cloudy",
        "humidity_percent": 28
    }

    #Convert to bytes
    plaintext = json.dumps(data).encode()

    #Encrypt using shared AES key
    cipher = AES.new(shared_key, AES.MODE_CTR)
    ciphertext = cipher.encrypt(plaintext)

    #Compute MAC
    mac_data = cipher.nonce + ciphertext
    tag = hmac.new(mac_key, mac_data, hashlib.sha256).digest()

    #Send encoded response
    response = {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }

    return jsonify(response)#Client's request response


#Run server
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5028) #Still using Stephen's last two student ID #'s