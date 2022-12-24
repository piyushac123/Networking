import argparse, os, base64, time
from Crypto import Random
from Crypto.Cipher import DES, DES3, AES

# https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256


def generateIV(block_size):
    return Random.new().read(block_size)


def encryptData(cipher, iv, indata):
    # Convert string to bytes
    plaintext = indata.encode("utf-8")
    # get the start time
    st = time.time()
    # To binary data
    ciphertext = base64.b64encode(iv + cipher.encrypt(plaintext))
    # get the end time
    et = time.time()
    return ciphertext, (et - st)


def decryptData(cipher, block_size, indata):
    # get the start time
    st = time.time()
    plaintext = cipher.decrypt(indata[block_size:])
    # get the end time
    et = time.time()
    # Convert bytes to string
    result = plaintext.decode("utf-8")
    return result, (et - st)


def getCipher(oper, algo, mode, passphrase, indata):
    # Convert string to bytes
    key = passphrase.encode("utf-8")
    if algo == "des":

        block_size = DES.block_size

        if oper == "enc":
            iv = generateIV(block_size)
        if oper == "dec":
            indata = base64.b64decode(indata)
            iv = indata[:block_size]

        if mode == "ecb":
            cipher = DES.new(key, DES.MODE_ECB)
        elif mode == "cbc":
            cipher = DES.new(key, DES.MODE_CBC, iv)

    elif algo == "3des":

        block_size = DES3.block_size

        if oper == "enc":
            iv = generateIV(block_size)
        if oper == "dec":
            indata = base64.b64decode(indata)
            iv = indata[:block_size]

        if mode == "ecb":
            cipher = DES3.new(key, DES3.MODE_ECB)
        elif mode == "cbc":
            cipher = DES3.new(key, DES3.MODE_CBC, iv)

    elif algo == "aes":

        block_size = AES.block_size

        if oper == "enc":
            iv = generateIV(block_size)
        if oper == "dec":
            indata = base64.b64decode(indata)
            iv = indata[:block_size]

        if mode == "ecb":
            cipher = AES.new(key, AES.MODE_ECB)
        elif mode == "cbc":
            cipher = AES.new(key, AES.MODE_CBC, iv)

    return cipher, iv, block_size, indata


def getPassPhrase(keysize):
    passLen = int(int(keysize) / 8)
    print("\nEnter passphrase of " + str(passLen) + " characters : ")
    while passphrase := input():
        if len(passphrase) >= passLen:
            break
        print("\nInvalid passphrase")
        print("\nEnter passphrase of " + str(passLen) + " characters : ")
    return passphrase[:passLen]


# MAIN FUNCTION
def main(oper, algo, mode, keysize, infile, outpath):
    print("\nEntered\n")
    print(
        "Args: \noper: "
        + oper
        + " \nalgo: "
        + algo
        + " \nmode: "
        + mode
        + " \nkeysize: "
        + keysize
        + " \ninfile: "
        + infile
        + " \noutpath: "
        + outpath
    )

    # Get passphrase from user
    passphrase = getPassPhrase(keysize)

    # Get input file data
    file = open(infile)
    indata = file.read()
    file.close()

    # Get cipher for algorithm and mode
    cipher, iv, block_size, indata = getCipher(oper, algo, mode, passphrase, indata)

    # Encrypt or Decrypt
    if oper == "enc":
        outdata, exec_time = encryptData(cipher, iv, indata)
        outdata = (outdata).decode("utf-8")
    elif oper == "dec":
        outdata, exec_time = decryptData(cipher, block_size, indata)

    input_file = infile[(infile.find("/", infile.find("/") + 1) + 1) :]

    file = open("records.txt", "a")
    file.write(
        oper
        + "_"
        + algo
        + "_"
        + mode
        + "_"
        + keysize
        + "_"
        + input_file
        + "\t"
        + str(exec_time)
        + "\n"
    )
    file.close()

    # Creating a file
    # Put data in output file - can use file name as oper_algo_mode_keysize_infile
    file = open(
        outpath
        + "/"
        + oper
        + "_"
        + algo
        + "_"
        + mode
        + "_"
        + keysize
        + "_"
        + input_file,
        "w",
    )
    file.write(outdata)
    file.close()


# Starting position
# Cryptographic Encryption-Decryption Analysis
if __name__ == "__main__":
    """
    Args :
    1. oper - operations with value 'enc' or 'dec'
    2. algo - algorithm with value 'des', '3des' or 'aes'
    3. mode - mode with value 'ecb' or 'cbc'
    4. keysize - keysizes in bits for des(64), 3des(192) or aes(128, 192, 256)
    5. infile - input file to be encrypted or decrypted
    6. outpath - output file path
    """
    parser = argparse.ArgumentParser(
        description="Cryptographic Encryption-Decryption Analysis"
    )

    # Argument extraction
    parser.add_argument(
        "-p",
        "--oper",
        help="enc/dec",
        type=str,
        action="store",
        required=False,
        default="enc",
    )
    parser.add_argument(
        "-a",
        "--algo",
        help="des/3des/aes",
        type=str,
        action="store",
        required=False,
        default="des",
    )
    parser.add_argument(
        "-m",
        "--mode",
        help="ecb/cbc",
        type=str,
        action="store",
        required=False,
        default="ecb",
    )
    parser.add_argument(
        "-k",
        "--keysize",
        help="64/128/192/256",
        type=str,
        action="store",
        required=False,
        default="64",
    )
    parser.add_argument(
        "-i",
        "--infile",
        help="input text file",
        type=str,
        action="store",
        required=False,
        default="../testcases/10K/test_10K_1.txt",
    )
    parser.add_argument(
        "-o",
        "--outpath",
        help="output file path",
        type=str,
        action="store",
        required=False,
        default="../testcases_output/10K",
    )

    args = parser.parse_args()

    if not args.oper:
        parser.print_help()
        print(
            "\nOperations not found: %s\n"
            % args.oper
        )
        parser.exit(1)
    if not args.algo:
        parser.print_help()
        print(
            "\nAlgorithm not found: %s\n"
            % args.algo
        )
        parser.exit(1)
    if not args.mode:
        parser.print_help()
        print(
            "\nMode not found: %s\n"
            % args.mode
        )
        parser.exit(1)
    if not args.keysize:
        parser.print_help()
        print(
            "\nKey size not found: %s\n"
            % args.keysize
        )
        parser.exit(1)
    if not os.path.exists(args.infile):
        parser.print_help()
        print(
            "\nInput file not found: %s\n"
            % args.infile
        )
        parser.exit(1)
    if not args.outpath:
        parser.print_help()
        print(
            "\nOutput file path not found: %s\n"
            % args.outpath
        )
        parser.exit(1)

    # Pass argument into main function
    main(args.oper, args.algo, args.mode, args.keysize, args.infile, args.outpath)
