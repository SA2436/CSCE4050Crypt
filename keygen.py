from Crypto.PublicKey import RSA #Like in Homework #1 but not for OTP

#Generate RSA key pair (2048 bits)
key = RSA.generate(2048)

#Extract secret key with generated RSA key pair 
secret_key = key.export_key()

#Extract public key with generated RSA key pair
public_key = key.publickey().export_key()

#Save secret key to "secret.key" file
with open("secret.key", "wb") as f:
    f.write(secret_key)

#Save the public key also to "private.key" file
with open("public.key", "wb") as f:
    f.write(public_key)
#Print when keys successfully generated
print("Secret and Public keys generated successful!")