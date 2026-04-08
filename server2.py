#This will be the server for client to GET the weather info
from flask import Flask, jsonify # install flask and create REST server
#using flask, install flask before running
#Task 2 Hardcode a pre-shared secret key, AES-CTR encryption, HMAC-SHA256 integrity, Encrypt-then-MAC
from Crypto.Cipher import AES #AES encryption
from Crypto.Random import get_random_bytes #Random IV
#Task 2.2 - 2.8ChatGPT fixed our code with the encryption by encoding binary into text and convert python dictionary to JSON string
import base64, json 
#Task 2.3 - 2.8 HMAC intergrity communications for computing MAC 
import hmac 
import hashlib

#TODO for different steps in Task 2 REMOVE (#) under the appropriate task to run

#Task 1-4 for flask run
app = Flask(__name__)

#Task 2 Step 1 - 8 Hardcode a pre-shared secret key 
secretKey = b'28282828282828282828282828282828' #Using the same method 32-byte key from Homework 5 using the last two student ID 
#FOR: Task 2.8 
#mac_key = b'cadc3239e73e53622d0664dff2651767f618a438f00ede9a6541fb1cb4835b05' #Hardcoded for ease input from tag.txt from previce steps on task 2

#Task 1-4 Weather endpoint returning a static JSON payload with weather Denton data 
@app.route('/weather', methods=['GET'])
def weather():
    data = {
        "location": "Denton, TX",
        "temperature_c": 10,
        "temperature_f": 50,
        "condition": "Partly Cloudy",
        "humidity_percent": 28  #Add with Stephen Alonso's last two of Student ID # digits (28) (Edit)
    }
    #Task 2 Step 2 and 6 #Encrypt PT with AES-CTR to only provide confidentiality
    plaintext = json.dumps(data).encode() #Fix with ChatGPT to converting python dictionary to JSON string to bytes instead of doing bytes.fromhex
    #Use the line below if running into errors for steps 2-6
    #plaintext = json.dumps(data, sort_keys=True).encode()

    #Task 2.2 
    cipher = AES.new(secretKey, AES.MODE_CTR) #AES-CTR from homework 5 with the secret key and generate random nonce 
    ciphertext = cipher.encrypt(plaintext) #AES-CTR encryption PT to CT

    #FOR Task 2 step 3 and 6 Compute HMAC-SHA256 tag
    #tag = hmac.new(secretKey, plaintext, hashlib.sha256).hexdigest()
    #Save HMAC-SHA256 tag into tag.txt for later project use
    # with open("tag.txt", "w") as f:
    #    f.write(tag)

    #FOR Task 2.6 MAC encrypted with nonce and computed ciphertext (Encrypt-then-MAC)
    #data_mac = cipher.nonce + ciphertext
    #FOR Task 2.6 MAC encrypted with nonce and computed ciphertext
    #tag = hmac.new(mac_key, data_mac, hashlib.sha256).digest()#Task 2.6 new computed mac key to push to response.bin (FIX with ChatGPT)

    enc_data = {
        #Encoding all the binary data to Base64 (advice from GeeksfrGeeks.org and ChatGPT) instead of ChaCha20 
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        #FOR Task 2.3
        #"tag": base64.b64encode(tag).decode()
    }
    #Task 2.6 records server's response
    #with open("response.bin", "wb") as f:
        #f.write(cipher.nonce + tag + ciphertext)

    #FOR Task2.3 ONLY
    #return jsonify({ "data": data, "tag": tag })
    #For every other Task 2 steps
    return jsonify(enc_data) #send JSON response to client when requested 

    #From previous task steps
    #return jsonify(enc_data) 
    
    

    

    #return jsonify({"data": data, "tag": tag}) #send JSON response to client when requested 

if __name__ == '__main__': #Server listens to a localhost (50)
    app.run(host='127.0.0.1', port=5028)  # Add with Stephen Alonso's Last two Student ID # digits (28)(Edit)
