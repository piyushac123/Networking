import os, json
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

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


# Generate Public and Private Key with values of n,e,d
def generateNED(path, publicKey, privateKey):
    file_out = open(path + "/public.json", "w")
    json.dump(publicKey, file_out)
    file_out.close()

    # Get json file data
    # file_out = open(path + "/public.json", "r")
    # pk = json.load(file_out)
    # file_out.close()
    # print(pk["e"])

    file_out = open(path + "/private.json", "w")
    json.dump(privateKey, file_out)
    file_out.close()


def generateRSAKey(name, more):
    path = "keys/" + name
    if not os.path.exists(path):
        # Create a new directory because it does not exist
        os.makedirs(path)

    key = RSA.generate(2048)
    publicKey = {"n": key.n, "e": key.e}
    privateKey = {"n": key.n, "d": key.d}
    if more == "y":
        generateNED(path, publicKey, privateKey)

    generatePrivateKey(path, key)
    generatePublicKey(path, key)

    # Way of digital signature and further retrieval of encrypted data
    # str1 = "Hello world!!!"
    # abc = int.from_bytes(bytes(str1, "UTF-8"), byteorder='big')
    # Hash certificate
    # hash_cert = SHA256.new()
    # hash_cert.update(str1.encode("utf-8"))
    # hash_cert = int.from_bytes(hash_cert.digest(), byteorder='big')
    # enc_str1 = pow(abc, privateKey["d"], privateKey["n"])
    # dec_str1 = pow(enc_str1, publicKey["e"], publicKey["n"])
    # print(str(dec_str1.to_bytes(abc.bit_length(), byteorder='big'), "UTF-8"))
