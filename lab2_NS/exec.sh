#!/bin/sh

while getopts c: flag
do
    case "${flag}" in
        c) choice=${OPTARG};;
    esac
done

if [ -z "$choice" ]; then choice=1; fi

case $choice in
    # CA execution
    1)
        python code/CertAuth.py -p 12345 -o 'ca_records.txt'
        ;;
    # sender execution
    2)
        python code/client.py -n piyush -m S -a 127.0.0.1 -p 12345 -q 23456
        ;;
    # receiver execution
    3)
        python code/client.py -n aakash -m R -i 'inputfile.txt' -d 127.0.0.1 -q 23456 -s 'outenc.txt' -o 'outfile.txt' -a 127.0.0.1 -p 12345
        ;;
esac