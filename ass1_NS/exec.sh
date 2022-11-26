#!/bin/sh

python code/cryptoAlgo.py -p enc -a 3des -m ecb -k 192 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
# python code/cryptoAlgo.py -p dec -a aes -m ecb -k 128 -i 'testcases_output/10K/enc_aes_ecb_128_test_10K_1.txt' -o 'testcases/10K'
# python code/cryptoAlgo.py --oper enc --algo des --mode ecb --keysize 56 --infile '../testcases/10K/test_10K_1.txt' --outfile '../testcases_output/10K/otest_10K_1.txt'