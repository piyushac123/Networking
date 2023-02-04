import os, csv

oper = ["enc", "dec"]
algo = ["des", "3des", "aes"]
mode = ["ecb", "cbc"]
keysize = [64, 128, 192, 256]
input_dir = ["testcases/10K", "testcases/1M"]
ky = "piyushac8765432112345678cahsuyip"


def generateBulkResult():
    for a in algo:
        if a == "des":
            ks = [keysize[0]]
        elif a == "3des":
            ks = [keysize[2]]
        elif a == "aes":
            ks = keysize[1:]

        for k in ks:

            for m in mode:

                for i in input_dir:

                    for filename in os.listdir(i):
                        f = os.path.join(i, filename)
                        # checking if it is a file
                        if os.path.isfile(f):
                            cmd = (
                                "python code/cryptoAlgo.py -p enc -a "
                                + str(a)
                                + " -m "
                                + str(m)
                                + " -k "
                                + str(k)
                                + " -i '"
                                + str(f)
                                + "' -o 'testcases_output/demo' -y "
                                + str(ky)
                            )
                            infile = str(f)[
                                (str(f).find("/", str(f).find("/") + 1) + 1) :
                            ]
                            infile = (
                                "testcases_output/demo/enc_"
                                + str(a)
                                + "_"
                                + str(m)
                                + "_"
                                + str(k)
                                + "_"
                                + infile
                            )
                            os.system(cmd)
                            cmd = (
                                "python code/cryptoAlgo.py -p dec -a "
                                + str(a)
                                + " -m "
                                + str(m)
                                + " -k "
                                + str(k)
                                + " -i '"
                                + infile
                                + "' -o 'testcases_output/demo' -y "
                                + str(ky)
                            )
                            os.system(cmd)


# MAIN FUNCTION
def main():
    os.system("sh exec.sh -c 22")

    # Generate bulk results
    generateBulkResult()

    # with open('records.csv', newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         print(row)


# Starting position
# Produce Cryptographic Encryption-Decryption Analysis Result
if __name__ == "__main__":
    # Pass argument into main function
    main()
