import requests
#Task 2 Hardcode a pre-shared secret key, AES-CTR encryption, HMAC-SHA256 integrity, Encrypt-then-MAC
from Crypto.Cipher import AES
import base64, json

#Task 2 Step 1 Hardcode a pre-shared secret key same from the server
secretKey = b'28282828282828282828282828282828' #Using the same method 16-byte key from Homework 5 using the last two student ID 

url = "http://127.0.0.1:5028/weather"  # Add the last two digits with Stephen Alonso's student ID (Edit)

response = requests.get(url).json() #Send GET request to the weather (edited with the help from ChatGPT to GET the weather data)


#Fix from ChatGPT to decoding the base64 value from server2 also got rid of the if and else statement due to errors
nonce = base64.b64decode(response['nonce'])
ciphertext = base64.b64decode(response['ciphertext'])

#Initailize and store the AES-CTR cipher from server to then decrypt and display weather data
cipher = AES.new(secretKey, AES.MODE_CTR, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)

print("Decrypted message:") #Print out the indicated decrypted message
print(json.loads(plaintext)) #Print Successful getting weather info from server

