import argparse, base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
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


def prepareCert(req):
    print(req)
    res = "### 302 ###"

    private_key = RSA.import_key(open("keys/CA/private.pem").read())
    # Decrypt with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)

    dec_name = req[2].encode("utf-8")
    # OR dec_name = bytes(req[2], "UTF-8")

    dec_name = base64.b64decode(dec_name)
    dec_name = cipher_rsa.decrypt(dec_name).decode("utf-8")

    print(dec_name)

    # file_out = open("keys/" + name + "/public.pem", "r")
    # req += file_out.read() + "\n"
    # file_out.close()

    # public_key = RSA.import_key(open("keys/CA/public.pem").read())
    # # Encrypt with the public RSA key
    # cipher_rsa = PKCS1_OAEP.new(public_key)
    # enc_name = cipher_rsa.encrypt(name.encode("utf-8"))

    # req += "### " + str(enc_name) + " ###\n"
    # req += "*****"

    return req


# MAIN FUNCTION
def main(caport, recordFile):
    print("\nEntered\n")
    print("Args: \ncaport: " + caport + " \nrecordFile: " + recordFile)
    keyGen.generateRSAKey("CA")
    socket = conn.Tcp_server_connect(5, int(caport))
    while True:
        client = conn.Tcp_server_next(socket)
        result = conn.Tcp_Read(client)
        results = separateResult(result)
        if results[0] == "301":
            prepareCert(results)
        conn.Tcp_Close(client)


# Starting position
# PKI Certificate Authority
if __name__ == "__main__":
    """
    Args :
    1. p - CA listening port
    2. o - CA activity records
    """
    parser = argparse.ArgumentParser(description="PKI Certificate Authority")

    # Argument extraction
    parser.add_argument(
        "-p",
        help="CA port",
        type=str,
        action="store",
        required=False,
        default="12345",
    )
    parser.add_argument(
        "-o",
        help="CA activity records",
        type=str,
        action="store",
        required=False,
        default="ca_records.txt",
    )

    args = parser.parse_args()

    if not args.p:
        parser.print_help()
        print("\CA port not found: %s\n" % args.p)
        parser.exit(1)
    if not args.o:
        parser.print_help()
        print("\nCA record file name not found: %s\n" % args.o)
        parser.exit(1)

    # Pass argument into main function
    main(args.p, args.o)
