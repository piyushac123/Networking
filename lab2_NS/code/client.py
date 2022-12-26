import argparse, json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

# https://www.geeksforgeeks.org/how-to-import-a-python-module-given-the-full-path/
from importlib.machinery import SourceFileLoader

# imports the module from the given path
R = SourceFileLoader("receiver", "code/helper/receiver.py").load_module()
S = SourceFileLoader("sender", "code/helper/sender.py").load_module()
K = SourceFileLoader("keyGen", "code/helper/keyGen.py").load_module()


def prepareReqCert(name):
    req = "| 301 |\n"

    file_out = open("keys/" + name + "/public.pem", "r")
    req += file_out.read() + "\n"
    file_out.close()

    public_key = RSA.import_key(open("keys/CA/public.pem").read())
    # Encrypt with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(public_key)
    enc_name = cipher_rsa.encrypt(name.encode("utf-8"))

    req += "| " + str(enc_name) + " |\n"
    req += "*****"

    # private_key = RSA.import_key(open("keys/CA/private.pem").read())
    # # Decrypt with the private RSA key
    # cipher_rsa = PKCS1_OAEP.new(private_key)
    # dec_name = cipher_rsa.decrypt(enc_name).decode("utf-8")

    return req


# def clientToClientCommunication():
#     print("clientToClientCommunication")


# MAIN FUNCTION
def main(args):
    print("\nEntered\n")
    print("Args: ")
    for val in args.keys():
        print(val + ": " + args[val])

    # Key generation
    K.generateRSAKey(args["n"])

    # Certificate Authorization
    req = prepareReqCert(args["n"])
    R.handleReceiver(args["a"], int(args["p"]), req)
    # file_out = open("keys/"+args["n"]+"/certificate", "wb")
    # file_out.write(R.handleReceiver(args["a"], int(args["p"]), req))
    # file_out.close()

    # clientToClientCommunication()


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
