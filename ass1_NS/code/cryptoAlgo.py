import argparse, os
from Crypto.Cipher import DES, DES3, AES


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


# Starting position
# Cryptographic Encryption-Decryption Analysis
if __name__ == "__main__":
    """
    Args :
    1. oper - operations with value 'enc' or 'dec'
    2. algo - algorithm with value 'des', '3des' or 'aes'
    3. mode - mode with value 'ecb' or 'cbc'
    4. keysize - keysizes in bits for des(64), 3des(168) or aes(128, 192, 256)
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
        help="64/168/128/192/256",
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
            "\nOperations not found: %s\nPlease compile the target P4 program first."
            % args.oper
        )
        parser.exit(1)
    if not args.algo:
        parser.print_help()
        print(
            "\nAlgorithm not found: %s\nPlease compile the target P4 program first."
            % args.algo
        )
        parser.exit(1)
    if not args.mode:
        parser.print_help()
        print(
            "\nMode not found: %s\nPlease compile the target P4 program first."
            % args.mode
        )
        parser.exit(1)
    if not args.keysize:
        parser.print_help()
        print(
            "\nKey size not found: %s\nPlease compile the target P4 program first."
            % args.keysize
        )
        parser.exit(1)
    if not os.path.exists(args.infile):
        parser.print_help()
        print(
            "\nInput file not found: %s\nPlease compile the target P4 program first."
            % args.infile
        )
        parser.exit(1)
    if not args.outpath:
        parser.print_help()
        print(
            "\nOutput file path not found: %s\nPlease compile the target P4 program first."
            % args.outpath
        )
        parser.exit(1)

    # Pass argument into main function
    main(args.oper, args.algo, args.mode, args.keysize, args.infile, args.outpath)