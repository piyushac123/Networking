import os, csv
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
    lst.append(df1[df1["algorithm"] == "3des"]["exec_time"].mean())\

    df1 = df1[df1["algorithm"] == "aes"]
    lst.append(df1[df1["keysize"] == 128]["exec_time"].mean())
    lst.append(df1[df1["keysize"] == 192]["exec_time"].mean())
    lst.append(df1[df1["keysize"] == 256]["exec_time"].mean())

    category = ['DES-64', '3DES-192', 'AES-128', 'AES-192', 'AES-256']

    d = {'category' : category, 'mean': lst}
    df_enc_ecb_10K = pd.DataFrame(data=d)

    return df_enc_ecb_10K

def generateGraph(df_enc_ecb_10K):
    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(df_enc_ecb_10K['category'], df_enc_ecb_10K['mean'], color ='maroon',
            width = 0.4)
    
    plt.xlabel("Category")
    plt.ylabel("Mean Block encryption time (in secs)")
    plt.title("Encryption of 10K file using ECB mode")

    if not os.path.exists("testcases_output/plots"):
        # Create a new directory because it does not exist
        os.makedirs("testcases_output/plots")

    plt.savefig('testcases_output/plots/enc_ecb_10K.png')

# MAIN FUNCTION
def main():
    os.system("sh exec.sh -c 22")

    if not os.path.exists("testcases_output/demo"):
        # Create a new directory because it does not exist
        os.makedirs("testcases_output/demo")


    # Generate bulk results
    generateBulkResult()

    # Read csv file data in dataframe
    df = pd.read_csv('records.csv')

    # Add new column - filesize
    for ind in range(df.shape[0]):
        if "10K" in df.loc[ind, "file"]:
            df.loc[ind, "filesize"] = "10K"
        elif "1M" in df.loc[ind, "file"]:
            df.loc[ind, "filesize"] = "1M"

    # Generate graph for different algorithms for - Encryption of 10K file using ECB mode
    df_enc_ecb_10K = refineEncEcb10K(df)
    generateGraph(df_enc_ecb_10K)


    # with open('records.csv', newline='') as csvfile:
    #     reader = csv.DictReader(csvfile)
    #     for row in reader:
    #         print(row)


# Starting position
# Produce Cryptographic Encryption-Decryption Analysis Result
if __name__ == "__main__":
    # Pass argument into main function
    main()
