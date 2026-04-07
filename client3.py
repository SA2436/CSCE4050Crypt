import requests #Send HTTP requests 
#Task 2 Hardcode a pre-shared secret key, AES-CTR encryption, HMAC-SHA256 integrity, Encrypt-then-MAC
from Crypto.Cipher import AES # AES decryption
import base64, json
#Task 2.3 HMAC integrity communication for computing MAC
import hmac
import hashlib

#Task 3 Step 2 - Use RSA secret key from server3.py and key_exchange
with open("response.bin", "rb") as f:
    secretKey = f.read()
    
mac_key = b'cadc3239e73e53622d0664dff2651767f618a438f00ede9a6541fb1cb4835b05' #Hardcoded for ease input from tag.txt from previce steps on task 2

url = "http://127.0.0.1:5028/weather"  # Add the last two digits with Stephen Alonso's student ID (Edit)
#url = "http://127.0.0.1:5029/weather" # For task 2.4 to connect to server_fake

res = requests.get(url) #Send GET request to the weather (edited with the help from ChatGPT to GET the weather data)
print("Raw response: ") #Fix to see what on the server2.py is bugging (ChatGPT)
print(res.text)

response = res.json()

nonce = base64.b64decode(response['nonce'])
ciphertext = base64.b64decode(response['ciphertext'])
tag = base64.b64decode(response['tag'])

#Verify new computed MAC
data_mac = nonce + ciphertext
new_mac = hmac.new(mac_key, data_mac, hashlib.sha256).digest()

#Test prints the tags should not match
if new_mac != tag:
    print("Failed integrity test")
    print("Client will not be able to access data to mismatch data")
    exit()

#Decryption for Task 2.6 from task 2.2
cipher = AES.new(secretKey, AES.MODE_CTR, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)

#Print out authenticated server
print("Authentication Successful")
print(json.loads(plaintext)) #ChatGPT fix to printing out the authenticated server

