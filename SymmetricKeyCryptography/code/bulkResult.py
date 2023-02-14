import os, csv, math
import pandas as pd
import matplotlib.pyplot as plt

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


def refineEncEcb10K(df):
    df1 = df[df["operation"] == "enc"]
    df1 = df1[df1["mode"] == "ecb"]
    df1 = df1[df1["filesize"] == "10K"]

    lst = []
    lst.append(df1[df1["algorithm"] == "des"]["exec_time"].mean())
    lst.append(df1[df1["algorithm"] == "3des"]["exec_time"].mean())
    df1 = df1[df1["algorithm"] == "aes"]
    lst.append(df1[df1["keysize"] == 128]["exec_time"].mean())
    lst.append(df1[df1["keysize"] == 192]["exec_time"].mean())
    lst.append(df1[df1["keysize"] == 256]["exec_time"].mean())

    category = ["DES-64", "3DES-192", "AES-128", "AES-192", "AES-256"]

    d = {"category": category, "mean": lst}
    df_enc_ecb_10K = pd.DataFrame(data=d)

    return df_enc_ecb_10K


def refineDecEcb10K(df):
    df1 = df[df["operation"] == "dec"]
    df1 = df1[df1["mode"] == "ecb"]
    df1 = df1[df1["filesize"] == "10K"]

    lst = []
    lst.append(df1[df1["algorithm"] == "des"]["exec_time"].mean())
    lst.append(df1[df1["algorithm"] == "3des"]["exec_time"].mean())
    df1 = df1[df1["algorithm"] == "aes"]
    lst.append(df1[df1["keysize"] == 128]["exec_time"].mean())
    lst.append(df1[df1["keysize"] == 192]["exec_time"].mean())
    lst.append(df1[df1["keysize"] == 256]["exec_time"].mean())

    category = ["DES-64", "3DES-192", "AES-128", "AES-192", "AES-256"]

    d = {"category": category, "mean": lst}
    df_dec_ecb_10K = pd.DataFrame(data=d)

    return df_dec_ecb_10K


def refineDes10K64(df):
    df1 = df[df["algorithm"] == "des"]
    df1 = df1[df1["filesize"] == "10K"]

    lst = []

    df2 = df1[df1["operation"] == "enc"]
    lst.append(df2[df2["mode"] == "ecb"]["exec_time"].mean())
    lst.append(df2[df2["mode"] == "cbc"]["exec_time"].mean())
    df2 = df1[df1["operation"] == "dec"]
    lst.append(df2[df2["mode"] == "ecb"]["exec_time"].mean())
    lst.append(df2[df2["mode"] == "cbc"]["exec_time"].mean())

    category = ["ENC-ECB", "ENC-CBC", "DEC-ECB", "DEC-CBC"]

    d = {"category": category, "mean": lst}
    df_des_64_10K = pd.DataFrame(data=d)

    return df_des_64_10K


def refineDes64(df):
    df1 = df[df["algorithm"] == "des"]

    lst = []

    df2 = df1[df1["operation"] == "enc"]
    lst.append(df2[df2["filesize"] == "10K"]["exec_time"].mean())
    lst.append(df2[df2["filesize"] == "1M"]["exec_time"].mean())

    df2 = df1[df1["operation"] == "dec"]
    lst.append(df2[df2["filesize"] == "10K"]["exec_time"].mean())
    lst.append(df2[df2["filesize"] == "1M"]["exec_time"].mean())

    category = ["ENC-10K", "ENC-1M", "DEC-10K", "DEC-1M"]

    d = {"category": category, "mean": lst}
    df_des_64 = pd.DataFrame(data=d)

    return df_des_64


def generateGraph(df, ylabel, title, img):
    fig = plt.figure(figsize=(10, 5))

    lst = []
    for i in range(df.shape[0]):
        lst.append(
            df.loc[i, "category"]
            + "\n"
            + str((math.ceil(df.loc[i, "mean"] * math.pow(10, 6)) / math.pow(10, 6)))
        )

    # creating the bar plot
    plt.bar(lst, df["mean"], color="maroon", width=0.4)

    plt.xlabel("Category")
    plt.ylabel(ylabel)
    plt.title(title)

    if not os.path.exists("testcases_output/plots"):
        # Create a new directory because it does not exist
        os.makedirs("testcases_output/plots")

    plt.savefig("testcases_output/plots/" + img)


# MAIN FUNCTION
def main():
    os.system("sh exec.sh -c 22")

    if not os.path.exists("testcases_output/demo"):
        # Create a new directory because it does not exist
        os.makedirs("testcases_output/demo")

    # Generate bulk results
    generateBulkResult()

    # Read csv file data in dataframe
    df = pd.read_csv("records.csv")

    # Add new column - filesize
    for ind in range(df.shape[0]):
        if "10K" in df.loc[ind, "file"]:
            df.loc[ind, "filesize"] = "10K"
        elif "1M" in df.loc[ind, "file"]:
            df.loc[ind, "filesize"] = "1M"

    # Generate graph for different algorithms for - Encryption of 10K file using ECB mode
    df_enc_ecb_10K = refineEncEcb10K(df)
    generateGraph(
        df_enc_ecb_10K,
        "Mean Block encryption time (in secs)",
        "For Encryption time analysis for algorithms - 10K file - ECB mode",
        "enc_ecb_10K.png",
    )

    # Generate graph for different algorithms for - Decryption of 10K file using ECB mode
    df_dec_ecb_10K = refineDecEcb10K(df)
    generateGraph(
        df_dec_ecb_10K,
        "Mean Block decryption time (in secs)",
        "For Decryption time analysis for algorithms - 10K file - ECB mode",
        "dec_ecb_10K.png",
    )

    # Generate graph for different algorithms for - Decryption of 10K file using ECB mode
    df_des_64_10K = refineDes10K64(df)
    generateGraph(
        df_des_64_10K,
        "Mean Block time (in secs)",
        "For Mode time analysis - DES - 64b keysize - 10K file",
        "des_64_10K.png",
    )

    # Generate graph for different algorithms for - Decryption of 10K file using ECB mode
    df_des_64 = refineDes64(df)
    generateGraph(
        df_des_64,
        "Mean Block time (in secs)",
        "For file size time analysis - DES - 64b keysize",
        "des_64.png",
    )

    # with open('records.csv', newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         print(row)


# Starting position
# Produce Cryptographic Encryption-Decryption Analysis Result
if __name__ == "__main__":
    # Pass argument into main function
    main()
