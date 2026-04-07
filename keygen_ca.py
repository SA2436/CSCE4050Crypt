from Crypto.PublicKey import RSA #Just like keygen.py 

#Generate CA key pair (2048 bits)
key = RSA.generate(2048)

#Save private key (secret)
with open("secret_ca.key", "wb") as f:
    f.write(key.export_key())

#Save public key
with open("public_ca.key", "wb") as f:
    f.write(key.publickey().export_key())

print("CA keys generated")