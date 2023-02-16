import argparse, base64, datetime, json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import Crypto.Random as rand
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

# from Crypto.Signature import pkcs1_15
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


def prepareCert(req, clientName):
    # prepare certificate
    res = "*** " + clientName + " *** "
    res += str(base64.b64encode(rand.get_random_bytes(8)), "UTF-8") + " ***\n"

    file_out = open("keys/" + clientName + "/public.pem", "r")
    res += file_out.read() + "\n*** "
    file_out.close()

    date = datetime.datetime.now()
    res += (
        str(int(date.strftime("%Y")))
        + "/"
        + date.strftime("%m")
        + "/"
        + date.strftime("%d")
        + " *** "
    )
    res += (
        str(int(date.strftime("%Y")) + 1)
        + "/"
        + date.strftime("%m")
        + "/"
        + date.strftime("%d")
        + " ***"
    )

    # Hash certificate
    hash_cert = SHA256.new(res.encode("utf-8"))

    if len(res) > 190:
        cnt = 190
    else:
        cnt = len(res)
    n = 0

    private_key = RSA.import_key(open("keys/CA/private.pem", "rb").read())

    public_key = RSA.import_key(open("keys/" + clientName + "/public.pem", "rb").read())
    cipher_rsa_pub = PKCS1_OAEP.new(public_key)

    # Digital signature for certificate
    # It is not possible to encrypt with a private key by definition.
    # https://stackoverflow.com/questions/60284761/python-rsa-key-recieved-the-key-but-getting-error-this-is-not-a-private-key
    # Digital signature by formula encryption using private key
    # https://cryptobook.nakov.com/digital-signatures/rsa-sign-verify-examples
    sign_cert = pkcs1_15.new(private_key).sign(hash_cert)
    sign_cert = base64.b64encode(sign_cert)
    sign_cert = str(sign_cert, "UTF-8")

    res += ", " + sign_cert

    result = ""

    # using splitted strings due to 'ValueError: Plaintext is too long' of RSA encrypt
    # Message can be of variable length, but not longer than the RSA modulus (in bytes) minus 2, minus twice the hash output size.
    # For instance, if you use RSA 2048 and SHA-256, the longest message you can encrypt is 190 byte long.
    while (len(res) - (n * cnt)) > 0:
        tmp = res[int(n * cnt) : int((n + 1) * cnt)]

        # Encrypt digitally signed certificate
        enc_cert = cipher_rsa_pub.encrypt(tmp.encode("utf-8"))
        enc_cert = base64.b64encode(enc_cert)
        enc_cert = str(enc_cert, "UTF-8")

        result += enc_cert + ", "
        n += 1

    return result


def prepareResponse(req):
    res = "### 302 ### "

    private_key = RSA.import_key(open("keys/CA/private.pem", "rb").read())
    # Decrypt with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(private_key)

    dec_name = req[2].encode("utf-8")
    # OR dec_name = bytes(req[2], "UTF-8")

    dec_name = base64.b64decode(dec_name)
    dec_name = cipher_rsa.decrypt(dec_name).decode("utf-8")

    res += dec_name + " ###\n"

    res += prepareCert(req, dec_name) + "\n###\n"
    res += "*****"

    return res


# MAIN FUNCTION
def main(caport, recordFile):
    print("\nEntered\n")
    print("Args: \ncaport: " + caport + " \nrecordFile: " + recordFile)
    keyGen.generateRSAKey("CA", "y")
    socket = conn.Tcp_server_connect(5, int(caport))
    while True:
        client = conn.Tcp_server_next(socket)

        # Get request for certificate
        result = conn.Tcp_Read(client)
        print("Certificate Request:")
        print(result)
        results = separateResult(result)
        if results[0] == "301":
            res = prepareResponse(results)

            # Send requested certificate
            conn.Tcp_Write(client, res)
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
