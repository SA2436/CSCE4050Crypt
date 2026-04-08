import requests #Send HTTP requests 
#Task 2 Hardcode a pre-shared secret key, AES-CTR encryption, HMAC-SHA256 integrity, Encrypt-then-MAC
from Crypto.Cipher import AES # AES decryption
import base64, json
#Task 2.3 HMAC integrity communication for computing MAC
import hmac
import hashlib

#Task 2 Step 1 - 8 Hardcode a pre-shared secret key same from the server
secretKey = b'28282828282828282828282828282828' #Using the same method 32-byte key from Homework 5 using the last two student ID 
#FOR Task 2.6
#mac_key = b'cadc3239e73e53622d0664dff2651767f618a438f00ede9a6541fb1cb4835b05' #Hardcoded for ease input from tag.txt from previce steps on task 2

url = "http://127.0.0.1:5028/weather"  # Add the last two digits with Stephen Alonso's student ID (Edit)

#For task 2.4 to connect to server_fake
#url = "http://127.0.0.1:5029/weather" 

res = requests.get(url) #Send GET request to the weather (edited with the help from ChatGPT to GET the weather data)
#IF errors when running client#.py
#print("Raw response: ") #Fix to see what on the server2.py is bugging (From ChatGPT to view the response when running code)
#print(res.text)

response = res.json()

#Task 2.3 FOUR LINES BELOW:
#data = response['data']
#tag = response['tag']
#ciphertext = json.dumps(data, sort_keys=True).encode() #Fix with ChatGPT from mismatch data and tag
#decode_tag = hmac.new(secretKey, ciphertext, hashlib.sha256).hexdigest()

#FOR Task 2.2 & 2.6 Fix from ChatGPT to decoding the base64 value from server2 also got rid of the if and else statement due to errors
nonce = base64.b64decode(response['nonce'])
ciphertext = base64.b64decode(response['ciphertext'])

#FOR Task 2.6
#tag = base64.b64decode(response['tag'])

#FOR Task 2.6 Verify new computed MAC
#data_mac = nonce + ciphertext
#new_mac = hmac.new(mac_key, data_mac, hashlib.sha256).digest()

#FOR Task 2.6 Test prints the tags should not match
#if new_mac != tag:
    #print("Failed integrity test")
    #print("Client will not be able to access data to mismatch data, Exiting Now")
    #exit()

#FOR Task 2.2 & Task 2.6 Decryption 
cipher = AES.new(secretKey, AES.MODE_CTR, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)

#FOR Task 2.2 Initailize and store the AES-CTR cipher from server to then decrypt and display weather data
print("Decrypted message:") #Print out the indicated decrypted message
print(json.loads(plaintext)) #Print Successful getting weather info from server

#FOR Task 2.3 with if data was tampered or not tampered to match HMAC tag from the server's HMAC tag
#if decode_tag = tag:
    #print("Data authenticated with HMAC tag")
    #print(data)
#else:
    #print("Data has been tampered")

#FOR Task 2.6 Print out authenticated server TWO LINE BELOW:
#print("Authentication Successful")
#print(json.loads(plaintext)) #ChatGPT fix to printing out the authenticated server






