import argparse

# MAIN FUNCTION
def main(oper, algo, mode, keysize, infile, outfile):
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
        + " \noutfile: "
        + outfile
    )


# Starting position
# Cryptographic Encryption-Decryption Analysis
if __name__ == "__main__":
    """
    Args :
    1. oper - operations with value 'enc' or 'dec'
    2. algo - algorithm with value 'des', '3des' or 'aes'
    3. mode - mode with value 'ecb' or 'cbc'
    4. keysize - keysizes in bits for des(56), 3des(168) or aes(128, 192, 256)
    5. infile - input file to be encrypted or decrypted
    6. outfile - output file to be encrypted or decrypted
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
        help="56/168/128/192/256",
        type=str,
        action="store",
        required=False,
        default="56",
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
        "--outfile",
        help="output text file",
        type=str,
        action="store",
        required=False,
        default="../testcases_output/10K/otest_10K_1.txt",
    )

    args = parser.parse_args()

    # Pass argument into main function
    main(args.oper, args.algo, args.mode, args.keysize, args.infile, args.outfile)
