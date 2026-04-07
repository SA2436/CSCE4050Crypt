import requests #Send HTTP requests 
#Task 2 Hardcode a pre-shared secret key, AES-CTR encryption, HMAC-SHA256 integrity, Encrypt-then-MAC
from Crypto.Cipher import AES # AES decryption
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA #ChatGPT fix for importing RSA keys
from Crypto.Random import get_random_bytes
import base64, json
#Task 2.3 HMAC integrity communication for computing MAC
import hmac
import hashlib
from Crypto.Cipher import PKCS1_OAEP #Fix with ChatGPT

    
mac_key = b'cadc3239e73e53622d0664dff2651767f618a438f00ede9a6541fb1cb4835b05' #Hardcoded for ease input from tag.txt from previce steps on task 2


res = requests.get("http://127.0.0.1:5028/get_cert")
#print("Status:", res.status_code) For troubleshooting
#print("Raw response:", res.text) For troubleshooting
data = res.json()

#Get the cert and public key
cert = base64.b64decode(data["cert"])
pubkey_bytes = base64.b64decode(data["pubkey"])

# Load CA public key
with open("public_ca.key", "rb") as f:
    ca_pub = RSA.import_key(f.read())

# Decode Data certificate
cert = base64.b64decode(data["cert"])

# Split message and signature
message, signature = cert.split(b"\nSIGNATURE\n")

# Verify signature
h = SHA256.new(message)

try:
    pkcs1_15.new(ca_pub).verify(h, signature)
    print("Certificate verified")
except:
    print("Certificate verification failed")
    exit()

#Verify public key
server_pub = RSA.import_key(pubkey_bytes)

# Generate AES key
aesSecret_key = get_random_bytes(16)

rsa_cipher = PKCS1_OAEP.new(server_pub) #Imported with the help off ChatGPT to help decrypt RSA-AES cipher
encrypted_key = rsa_cipher.encrypt(aesSecret_key)

encoded_key = base64.b64encode(encrypted_key).decode()

#Send key
requests.post("http://127.0.0.1:5028/key", json={"key": encoded_key})

#From client3.py Task 3
res = requests.get("http://127.0.0.1:5028/weather")  #Send GET request to the weather 
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
cipher = AES.new(aesSecret_key, AES.MODE_CTR, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)

#Print out Verification of key communication
print("Secured Verification Communication Success")
print(json.loads(plaintext)) #ChatGPT fix to printing out the authenticated server
