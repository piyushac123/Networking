import argparse, json, base64, os, time
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

# https://www.geeksforgeeks.org/how-to-import-a-python-module-given-the-full-path/
from importlib.machinery import SourceFileLoader

# imports the module from the given path
conn = SourceFileLoader("socketConn", "code/helper/socketConn.py").load_module()
keyGen = SourceFileLoader("keyGen", "code/helper/keyGen.py").load_module()


def separateResult(result):
    results = []
    result = result[3:]
    pos = 0
    while pos != -1:
        pos = result.find("###")
        results.append(result[1 : (pos - 1)])
        result = result[(pos + 3) :]

    return results[:-1]


def generateIV(block_size):
    return Random.new().read(block_size)


def generateCipher(passphrase):
    # Convert string to bytes
    key = passphrase.encode("utf-8")

    block_size = AES.block_size
    iv = generateIV(block_size)

    # Will be using AES algorithm in CBC mode with key size 128B
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return cipher, iv


def getCipher(passphrase, iv):
    # Convert string to bytes
    key = passphrase.encode("utf-8")

    # Will be using AES algorithm in CBC mode with key size 128B
    cipher = AES.new(key, AES.MODE_CBC, iv)

    return cipher


def encryptData(cipher, iv, indata):
    # Convert string to bytes
    plaintext = indata.encode("utf-8")

    # To binary data
    # Working for 10KB, but not for 1KB
    ciphertext = base64.b64encode(iv + cipher.encrypt(plaintext))
    ciphertext = str(ciphertext, "UTF-8")

    return ciphertext


def decryptData(cipher, block_size, indata):
    plaintext = cipher.decrypt(indata)

    # Convert bytes to string
    result = plaintext.decode("utf-8")
    return result


def decrypt504Message(passphrase, indata):
    ciphertext = bytes(indata, "UTF-8")
    ciphertext = base64.b64decode(ciphertext)

    block_size = AES.block_size
    iv = ciphertext[:block_size]

    cipher = getCipher(passphrase, iv)
    indata = decryptData(cipher, block_size, ciphertext[block_size:])

    return indata


def prepare504Message(sender, passphrase, infile):
    res = "### 504 ### " + infile + " ###\n"

    private_key = RSA.import_key(open("keys/" + sender + "/private.pem", "rb").read())
    cipher_rsa = PKCS1_OAEP.new(private_key)

    passphrase = bytes(passphrase, "UTF-8")
    passphrase = base64.b64decode(passphrase)
    passphrase = cipher_rsa.decrypt(passphrase).decode("utf-8")

    # Cipher for given session key - using AES
    cipher, iv = generateCipher(passphrase)

    file_out = open(infile, "r")
    indata = file_out.read()
    file_out.close()

    # Encrypt file content using provided session key
    enc_data = encryptData(cipher, iv, indata)

    res += enc_data + "\n### *****"

    return res


def prepare503Message(sender, passphrase, infile):
    res = "### 503 ###\n"

    public_key = RSA.import_key(open("keys/" + sender + "/public.pem", "rb").read())
    cipher_rsa = PKCS1_OAEP.new(public_key)

    enc_cipher = cipher_rsa.encrypt(passphrase.encode("utf-8"))
    enc_cipher = base64.b64encode(enc_cipher)
    enc_cipher = str(enc_cipher, "UTF-8")

    res += enc_cipher + "\n### " + infile + "\n### *****"

    return res


def prepare502Message(name):
    res = "### 502 ### " + name + " ###\n"

    file_out = open("keys/" + name + "/certificate.txt", "r")
    signed_cert = file_out.read()
    file_out.close()

    res += signed_cert + "\n### *****"

    return res


def verifyCert(signed_cert):
    public_key = RSA.import_key(open("keys/CA/public.pem", "rb").read())
    cert = signed_cert.split(", ")

    # Hash certificate
    hash_cert = SHA256.new(cert[0].encode("utf-8"))

    cert_signed = bytes(cert[1], "UTF-8")
    cert_signed = base64.b64decode(cert_signed)
    try:
        # verify digital signature by CA's public key
        pkcs1_15.new(public_key).verify(hash_cert, cert_signed)
        print("The signature is valid.")
    except (ValueError, TypeError):
        print("The signature is not valid.")


def prepareAndStoreCert(results, clientName):
    signed_cert = ""
    private_key = RSA.import_key(
        open("keys/" + clientName + "/private.pem", "rb").read()
    )
    cipher_rsa = PKCS1_OAEP.new(private_key)

    # Decrypt certificate
    for cipher in results[2].split(", "):
        if cipher != "":
            dec_cert = bytes(cipher, "UTF-8")
            dec_cert = base64.b64decode(dec_cert)
            dec_cert = cipher_rsa.decrypt(dec_cert).decode("utf-8")

            signed_cert += dec_cert

    verifyCert(signed_cert)

    path = "keys/" + clientName
    if not os.path.exists(path):
        # Create a new directory because it does not exist
        os.makedirs(path)

    file_out = open(path + "/certificate.txt", "w")
    file_out.write(signed_cert)
    file_out.close()

    print("Certificate stored at " + path + "/certificate.txt")


def prepareReqCert(name):
    req = "### 301 ###\n"

    file_out = open("keys/" + name + "/public.pem", "r")
    req += file_out.read() + "\n"
    file_out.close()

    public_key = RSA.import_key(open("keys/CA/public.pem", "rb").read())
    # Encrypt with the public RSA key
    # Useful page -
    # https://stackoverflow.com/questions/62940069/python-rsa-encryption-with-pkcs1-oaep-pkcs1-v1-5-fails-to-decrypt-special-charac
    # https://docs.python.org/3/library/base64.html

    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_name = cipher_rsa.encrypt(name.encode("utf-8"))
    enc_name = base64.b64encode(enc_name)

    req += "### " + str(enc_name, "UTF-8") + " ###\n"
    req += "*****"

    return req


# MAIN FUNCTION
def main(args):
    print("\nEntered\n")
    print("Args: ")
    for val in args.keys():
        print(val + ": " + args[val])

    # Key generation
    keyGen.generateRSAKey(args["n"], "n")

    # Certificate Authorization
    req = prepareReqCert(args["n"])
    socket = conn.Tcp_client_connect(args["a"], int(args["p"]))

    # Request certificate
    conn.Tcp_Write(socket, req)
    print("Sent Request for Certificate to CA")

    # Receive certificate
    result = conn.Tcp_Read(socket)
    print("Received Certificate in Response from CA")
    print(result)
    results = separateResult(result)
    if results[0] == "302":
        prepareAndStoreCert(results, args["n"])
    conn.Tcp_Close(socket)

    # Client to Client Communication
    if args["m"] == "R":
        time.sleep(15)
        socket = conn.Tcp_client_connect(args["d"], int(args["q"]))

        # Request for Sender's certificate - 501
        req = "### 501 ### " + args["n"] + " ### *****"
        conn.Tcp_Write(socket, req)
        print("Sent Request for Certificate of Sender")

        # Receive certificate
        result = conn.Tcp_Read(socket)
        print("Received Sender's Certificate in Response")
        results = separateResult(result)

        # Verify authenticity of certificate - by digital signature of CA
        if results[0] == "502":
            verifyCert(results[2])

            # Request for file from Sender using session key - 503
            req = prepare503Message(results[1], args["y"], args["i"])
            time.sleep(1)
            conn.Tcp_Write(socket, req)
            print("Sent Request for File Content from Sender")

            # Receive file
            result = conn.Tcp_Read(socket)
            print("Received File Content in Response")
            results = separateResult(result)

            # Store encrypted and decrypted file
            if results[0] == "504":
                file_out = open(args["s"], "w")
                file_out.write(results[2])
                file_out.close()

                outdata = decrypt504Message(args["y"], results[2])

                file_out = open(args["o"], "w")
                file_out.write(outdata)
                file_out.close()

                print(
                    "Stored Encrypted File Content in - "
                    + args["s"]
                    + " -  and Decrypted File Content in - "
                    + args["o"]
                )

    elif args["m"] == "S":
        socket = conn.Tcp_server_connect(5, int(args["q"]))
        client = conn.Tcp_server_next(socket)

        # Get request for certificate
        result = conn.Tcp_Read(client)
        print("Received My Certificate Request")
        results = separateResult(result)

        if results[0] == "501":
            res = prepare502Message(args["n"])

            # Send requested certificate - 502
            time.sleep(1)
            conn.Tcp_Write(client, res)
            print("Sent Requested Certificate")

            # Get request for file
            result = conn.Tcp_Read(client)
            results = separateResult(result)
            print("Received Sender's File Content Request for File - " + results[2])

            # Send encrypted requested file - 504
            if results[0] == "503":
                res = prepare504Message(args["n"], results[1], results[2])
                # Send requested file data - 504
                time.sleep(1)
                conn.Tcp_Write(client, res)
                print("Sent Requested File Content")


# Starting position
# Client-side implementation
if __name__ == "__main__":
    """
    Args :
    - n : client name
    - m : Sender(S)/Receiver(R)
    - i : requested input file name
    - d : Sender's IP
    - q : Sender's Port
    - s : file to store encrypted content received
    - o : file to store decrypted content received
    - a : CA's IP
    - p : CA's Port
    - y : Passphrase
    """
    parser = argparse.ArgumentParser(description="Client-side implementation")

    # Argument extraction
    parser.add_argument(
        "-n",
        help="client name",
        type=str,
        action="store",
        required=True,
        default="Piyush",
    )
    parser.add_argument(
        "-m",
        help="Sender(S)/Receiver(R)",
        type=str,
        action="store",
        required=True,
        default="S",
    )
    parser.add_argument(
        "-a",
        help="CA's IP",
        type=str,
        action="store",
        required=True,
        default="127.0.0.1",
    )
    parser.add_argument(
        "-p",
        help="CA's Port",
        type=str,
        action="store",
        required=True,
        default="12345",
    )
    parser.add_argument(
        "-q",
        help="Sender's Port",
        type=str,
        action="store",
        required=True,
        default="23456",
    )
    parser.add_argument(
        "-i",
        help="requested input file name",
        type=str,
        action="store",
        required=False,
        default="input.txt",
    )
    parser.add_argument(
        "-d",
        help="Sender's IP",
        type=str,
        action="store",
        required=False,
        default="127.0.0.1",
    )
    parser.add_argument(
        "-s",
        help="Received content encrypted file",
        type=str,
        action="store",
        required=False,
        default="output_enc.txt",
    )
    parser.add_argument(
        "-o",
        help="Received content decrypted file",
        type=str,
        action="store",
        required=False,
        default="output_dec.txt",
    )
    parser.add_argument(
        "-y",
        help="passphrase",
        type=str,
        action="store",
        required=False,
        default="",
    )

    args = parser.parse_args()

    if not args.n:
        parser.print_help()
        print("\Client name not found: %s\n" % args.n)
        parser.exit(1)
    if not args.m:
        parser.print_help()
        print("\nClient choice not found: %s\n" % args.m)
        parser.exit(1)
    if not args.a:
        parser.print_help()
        print("\CA's IP not found: %s\n" % args.a)
        parser.exit(1)
    if not args.p:
        parser.print_help()
        print("\nCA's port not found: %s\n" % args.p)
        parser.exit(1)
    if not args.q:
        parser.print_help()
        print("\Sender's port not found: %s\n" % args.q)
        parser.exit(1)
    if args.m == "R":
        if not args.i:
            parser.print_help()
            print("\nInput file name name not found: %s\n" % args.i)
            parser.exit(1)
        if not args.d:
            parser.print_help()
            print("\Sender's IP not found: %s\n" % args.d)
            parser.exit(1)
        if not args.s:
            parser.print_help()
            print("\nReceived content encrypted file name not found: %s\n" % args.s)
            parser.exit(1)
        if not args.o:
            parser.print_help()
            print("\Received content decrypted file name not found: %s\n" % args.o)
            parser.exit(1)
        if not args.y:
            parser.print_help()
            print("\Passphrase not found: %s\n" % args.y)
            parser.exit(1)

    # Pass argument into main function
    main(vars(args))
