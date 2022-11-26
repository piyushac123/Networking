#!/bin/sh

python code/cryptoAlgo.py -p enc -a des -m ecb -k 64 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'
# python code/cryptoAlgo.py --oper enc --algo des --mode ecb --keysize 56 --infile '../testcases/10K/test_10K_1.txt' --outfile '../testcases_output/10K/otest_10K_1.txt'