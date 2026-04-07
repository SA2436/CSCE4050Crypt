from Crypto.PublicKey import RSA # Import RSA public key tools
from Crypto.Random import get_random_bytes # Generate random AES key
import base64 #Encode binary for sending over HTTP (Fix from ChatGPT to encode encrypted key)
import requests #For send HTTP request
from Crypto.Cipher import PKCS1_OAEP# Used for secure RSA encryption with padding (ChatGPT fix for RSA cipher)

#Generate random AES key (16 bytes)
aes_key = get_random_bytes(16)

#Load server's public.key generated public key
with open("public.key", "rb") as f:
    public_key = RSA.import_key(f.read())

#Create RSA cipher
rsa_cipher = PKCS1_OAEP.new(public_key)

#Encrypt AES key using RSA
encrypted_key = rsa_cipher.encrypt(aes_key)

#Encode encrypted key so it can be sent via JSON
encoded_key = base64.b64encode(encrypted_key).decode()

#Send encrypted key to server
url = "http://127.0.0.1:5028/key"

response = requests.post(url, json={"key": encoded_key})

#Save AES key locally to response.bin
print("Server response:", response.text)
with open("response.bin", "wb") as f:
    f.write(aes_key)