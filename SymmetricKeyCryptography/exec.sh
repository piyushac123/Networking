#!/bin/sh

while getopts c: flag
do
    case "${flag}" in
        c) choice=${OPTARG};;
    esac
done

if [ -z "$choice" ]; then choice=1; fi

# sometimes hv to change -i and -o
case $choice in
    1)
        python code/cryptoAlgo.py -p enc -a des -m ecb -k 64 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
        ;;
    2)
        python code/cryptoAlgo.py -p dec -a des -m ecb -k 64 -i 'testcases_output/10K/enc_des_ecb_64_test_10K_1.txt' -o 'testcases/10K'
        ;;
    3)
        python code/cryptoAlgo.py -p enc -a des -m cbc -k 64 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
        ;;
    4)
        python code/cryptoAlgo.py -p dec -a des -m cbc -k 64 -i 'testcases_output/10K/enc_des_cbc_64_test_10K_1.txt' -o 'testcases/10K'
        ;;
    5)
        python code/cryptoAlgo.py -p enc -a 3des -m ecb -k 192 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
        ;;
    6)
        python code/cryptoAlgo.py -p dec -a 3des -m ecb -k 192 -i 'testcases_output/10K/enc_3des_ecb_192_test_10K_1.txt' -o 'testcases/10K'
        ;;
    7)
        python code/cryptoAlgo.py -p enc -a 3des -m cbc -k 192 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
        ;;
    8)
        python code/cryptoAlgo.py -p dec -a 3des -m cbc -k 192 -i 'testcases_output/10K/enc_3des_cbc_192_test_10K_1.txt' -o 'testcases/10K'
        ;;
    9)
        python code/cryptoAlgo.py -p enc -a aes -m ecb -k 128 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
        ;;
    10)
        python code/cryptoAlgo.py -p dec -a aes -m ecb -k 128 -i 'testcases_output/10K/enc_aes_ecb_128_test_10K_1.txt' -o 'testcases/10K'
        ;;
    11)
        python code/cryptoAlgo.py -p enc -a aes -m cbc -k 128 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
        ;;
    12)
        python code/cryptoAlgo.py -p dec -a aes -m cbc -k 128 -i 'testcases_output/10K/enc_aes_cbc_128_test_10K_1.txt' -o 'testcases/10K'
        ;;
    13)
        python code/cryptoAlgo.py -p enc -a aes -m ecb -k 192 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
        ;;
    14)
        python code/cryptoAlgo.py -p dec -a aes -m ecb -k 192 -i 'testcases_output/10K/enc_aes_ecb_192_test_10K_1.txt' -o 'testcases/10K'
        ;;
    15)
        python code/cryptoAlgo.py -p enc -a aes -m cbc -k 192 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
        ;;
    16)
        python code/cryptoAlgo.py -p dec -a aes -m cbc -k 192 -i 'testcases_output/10K/enc_aes_cbc_192_test_10K_1.txt' -o 'testcases/10K'
        ;;
    17)
        python code/cryptoAlgo.py -p enc -a aes -m ecb -k 256 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
        ;;
    18)
        python code/cryptoAlgo.py -p dec -a aes -m ecb -k 256 -i 'testcases_output/10K/enc_aes_ecb_256_test_10K_1.txt' -o 'testcases/10K'
        ;;
    19)
        python code/cryptoAlgo.py -p enc -a aes -m cbc -k 256 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
        ;;
    20)
        python code/cryptoAlgo.py -p dec -a aes -m cbc -k 256 -i 'testcases_output/10K/enc_aes_cbc_256_test_10K_1.txt' -o 'testcases/10K'
        ;;
    21)
        python code/bulkResult.py
        ;;
    22)
        rm records.txt records.csv
        ;;
esac

# python code/cryptoAlgo.py -p enc -a 3des -m ecb -k 192 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
# python code/cryptoAlgo.py -p dec -a 3des -m ecb -k 192 -i 'testcases_output/10K/enc_3des_ecb_192_test_10K_1.txt' -o 'testcases/10K'
# python code/cryptoAlgo.py -p dec -a aes -m ecb -k 128 -i 'testcases_output/10K/enc_aes_ecb_128_test_10K_1.txt' -o 'testcases/10K'
# python code/cryptoAlgo.py --oper enc --algo des --mode ecb --keysize 56 --infile '../testcases/10K/test_10K_1.txt' --outfile '../testcases_output/10K/otest_10K_1.txt'