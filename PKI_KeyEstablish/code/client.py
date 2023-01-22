import argparse, json, base64, os, time
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
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


def prepareAndStoreCert(results, clientName):
    signed_cert = ""

    # Decrypt certificate
    private_key = RSA.import_key(
        open("keys/" + clientName + "/private.pem", "rb").read()
    )
    cipher_rsa = PKCS1_OAEP.new(private_key)
    for cipher in results[2].split(", "):
        dec_cert = bytes(cipher, "UTF-8")
        dec_cert = base64.b64decode(dec_cert)
        dec_cert = cipher_rsa.decrypt(dec_cert).decode("utf-8")
        signed_cert += dec_cert

    signed_cert = bytes(signed_cert, "UTF-8")
    signed_cert = base64.b64decode(signed_cert)

    path = "keys/" + clientName
    if not os.path.exists(path):
        # Create a new directory because it does not exist
        os.makedirs(path)

    file_out = open(path + "/certificate.txt", "wb")
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


def prepare502Message(name):
    res = "### 502 ### " + name + " ###\n"

    file_out = open("keys/" + name + "/certificate.txt", "rb")
    signed_cert = file_out.read()
    file_out.close()

    print(signed_cert)

    signed_cert = base64.b64encode(signed_cert)
    signed_cert = str(signed_cert, "UTF-8")

    res += signed_cert + "\n### *****"

    return res


# MAIN FUNCTION
def main(args):
    print("\nEntered\n")
    print("Args: ")
    for val in args.keys():
        print(val + ": " + args[val])

    # Key generation
    keyGen.generateRSAKey(args["n"])

    # Certificate Authorization
    req = prepareReqCert(args["n"])
    socket = conn.Tcp_client_connect(args["a"], int(args["p"]))

    # Request certificate
    conn.Tcp_Write(socket, req)

    # Receive certificate
    result = conn.Tcp_Read(socket)
    print("Certificate Response:")
    print(result)
    results = separateResult(result)
    prepareAndStoreCert(results, args["n"])
    conn.Tcp_Close(socket)

    # Client to Client Communication
    if args["m"] == "R":
        time.sleep(15)
        socket = conn.Tcp_client_connect(args["d"], int(args["q"]))

        # Request for Sender's certificate - 501
        req = "### 501 ### " + args["n"] + " ### *****"
        conn.Tcp_Write(socket, req)

        # Receive certificate
        result = conn.Tcp_Read(socket)
        print("Sender's Certificate Response:")
        print(result)
        results = separateResult(result)

        # if results[0] == "502":
        # Verify authenticity of certificate - by digital signature of CA
        # verifyCert()
        # public_key = RSA.import_key(open("keys/CA/public.pem", "rb").read())
        # cipher_rsa = PKCS1_OAEP.new(public_key)

        # signed_cert = bytes(results[2], "UTF-8")
        # signed_cert = base64.b64decode(signed_cert)

        # hash_cert = cipher_rsa.decrypt(signed_cert).decode("utf-8")

        # try:
        #     pkcs1_15.new(public_key).verify(hash_cert, signed_cert)
        #     print("The signature is valid.")
        # except (ValueError, TypeError):
        #     print("The signature is not valid.")

        # Generate session key - using AES
        # Request for file from Sender using session key - 503
        # Receive file
        # Store encrypted and decrypted file

    elif args["m"] == "S":
        socket = conn.Tcp_server_connect(5, int(args["q"]))
        client = conn.Tcp_server_next(socket)

        # Get request for certificate
        result = conn.Tcp_Read(client)
        print("My Certificate Request:")
        print(result)
        results = separateResult(result)

        if results[0] == "501":
            res = prepare502Message(args["n"])

            # Send requested certificate - 502
            conn.Tcp_Write(client, res)

            # Get request for file
            # Send encrypted requested file - 504


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

    # Pass argument into main function
    main(vars(args))
