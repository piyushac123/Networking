import os
from Crypto.PublicKey import RSA

# Generate Private Key
def generatePrivateKey(path, key):
    private_key = key.export_key()
    file_out = open(path + "/private.pem", "wb")
    file_out.write(private_key)
    file_out.close()


# Generate Public Key
def generatePublicKey(path, key):
    public_key = key.publickey().export_key()
    file_out = open(path + "/public.pem", "wb")
    file_out.write(public_key)
    file_out.close()


def generateRSAKey(name, more):
    path = "keys/" + name
    if not os.path.exists(path):
        # Create a new directory because it does not exist
        os.makedirs(path)

    key = RSA.generate(2048)
    generatePrivateKey(path, key)
    generatePublicKey(path, key)
