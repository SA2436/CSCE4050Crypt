from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

# Load server public key
with open("public.key", "rb") as f:
    pub_key_bytes = f.read()

# Convert to hex
pub_key_hex = pub_key_bytes.hex()

student_id = "10836328"  #Replaced with Stephen's 8-digit Student ID

# Create message
message = f"This public key: {pub_key_hex} belongs to {student_id}"

message_bytes = message.encode()

#Load CA private key
with open("secret_ca.key", "rb") as f:
    ca_key = RSA.import_key(f.read())

#Hash SHA 256 message
h = SHA256.new(message_bytes)

#Sign message
signature = pkcs1_15.new(ca_key).sign(h)

#Save cert with message + signature
with open("pk.cert", "wb") as f:
    f.write(message_bytes + b"\nSIGNATURE\n" + signature)

print("Certificate key generated")