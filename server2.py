#This will be the server for client to GET the weather info
from flask import Flask, jsonify # install flask
#using flask, install flask before running
#Task 2 Hardcode a pre-shared secret key, AES-CTR encryption, HMAC-SHA256 integrity, Encrypt-then-MAC
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes #Random IV
import base64, json #ChatGPT fixed our code with the encryption by encoding binary into text and convert python dictionary to JSON string

app = Flask(__name__)
#Weather endpoint returning a static JSON payload with weather Denton data

#Task 2 Step 1 Hardcode a pre-shared secret key 
secretKey = b'28282828282828282828282828282828' #Using the same method 16-byte key from Homework 5 using the last two student ID 


@app.route('/weather', methods=['GET'])
def weather():
    data = {
        "location": "Denton, TX",
        "temperature_c": 10,
        "temperature_f": 50,
        "condition": "Partly Cloudy",
        "humidity_percent": 28  #Add with Stephen Alonso's last two of Student ID # digits (28) (Edit)
    }
    #Task 2 Step 2 #Encrypt PT with AES-CTR to only provide confidentiality
    plaintext = json.dumps(data).encode() #Fix from ChatGPT to converting python dictionary to JSON string to bytes instead of doing bytes.fromhex
    cipher = AES.new(secretKey, AES.MODE_CTR) #AES-CTR from homework 5 with the secret key and generate random nonce 
    ciphertext = cipher.encrypt(plaintext) #AES-CTR encryption PT to CT

    enc_data = {
        #Encoding all the binary data to Base64 (advice from GeeksfrGeeks.org and ChatGPT) instead of ChaCha20 
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }
    
    return jsonify(enc_data)

if __name__ == '__main__': #Server listens to a localhost (50)
    app.run(host='127.0.0.1', port=5028)  # Add with Stephen Alonso's Last two Student ID # digits (28)(Edit)
