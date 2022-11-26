### Network Security
#### Assignment 1 - Lab1-1.pdf

- Command
    - python code/cryptoAlgo.py --oper enc --algo des --mode ecb --keysize 56 --infile '../testcases/10K/test_10K_1.txt' --outfile '../testcases_output/10K/otest_10K_1.txt'
    - python code/cryptoAlgo.py -p enc -a des -m ecb -k 64 -i 'testcases/10K/test_10K_1.txt' -o 'testcases_output/10K'

- Parameters
    1. oper - operations with value 'enc' or 'dec'
    2. algo - algorithm with value 'des', '3des' or 'aes'
    3. mode - mode with value 'ecb' or 'cbc'
    4. keysize - keysizes in bits for des(56), 3des(168) or aes(128, 192, 256)
    5. infile - input file to be encrypted or decrypted
    6. outpath - output file path

- Python Cryptographic Package - [PyCryptodome](https://www.pycryptodome.org/src/introduction)