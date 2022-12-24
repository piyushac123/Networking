import argparse

# MAIN FUNCTION
def main(caport, recordFile):
    print("\nEntered\n")
    print(
        "Args: \ncaport: "
        + caport
        + " \nrecordFile: "
        + recordFile
    )

# Starting position
# PKI Certificate Authority
if __name__ == "__main__":
    """
    Args :
    1. p - CA listening port
    2. o - CA activity records
    """
    parser = argparse.ArgumentParser(
        description="PKI Certificate Authority"
    )

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
        print(
            "\CA port not found: %s\n"
            % args.p
        )
        parser.exit(1)
    if not args.o:
        parser.print_help()
        print(
            "\nCA record file name not found: %s\n"
            % args.o
        )
        parser.exit(1)

    # Pass argument into main function
    main(args.p, args.o)