### Network Security

#### Assignment 2 - Lab2.pdf

- Quick Run

  - `sh exec.sh -c {choice}` - execute shell script
  - choice - 1 : execute CA
  - choice - 2 : execute sender
  - choice - 3 : execute receiver

- Executable example

  - `python code/CertAuth.py -p 12345 -o 'ca_records.txt'`
    - p : CA listening port
    - o : CA activity records
  - `python code/client.py -n piyush -m S -a 127.0.0.1 -p 12345 -q 23456`
    - n : client name
    - m : Sender(S)
    - a : CA's IP
    - p : CA's Port
    - q : client listening port
  - `python code/client.py -n aakash -m R -i 'input.txt' -d 127.0.0.1 -q 23456 -s 'output_enc.txt' -o 'output_dec.txt' -a 127.0.0.1 -p 12345`
    - n : client name
    - m : Receiver(R)
    - i : requested input file name
    - d : Sender's IP
    - q : Sender's Port
    - s : file to store encrypted content received
    - o : file to store decrypted content received
    - a : CA's IP
    - p : CA's Port

- Python Cryptographic Package - [PyCryptodome](https://www.pycryptodome.org/src/introduction)

- Steps

  - PKI Certificate Authority
    - Execute CA, client1(sender) and client2(receiver) code on seperate terminals/machine/virtual machines
    - Generate public and private key pair for CA and both clients
    - Send certificate request from both clients to CA
    - CA replies with filled appropriate fields in certificate
    - Clients stores certificate locally
    - After receiving certificate sleep for 15 seconds
  - Client-to-client certificate exchange and key exchange
    - Receiver send request to sender for sender's certificate
    - Sender replies with it's certificate
    - Receiver verifies sender's certificate
    - Receiver generate session key and send to sender
    - Sender replies with encrypted file content using session key
    - Receiver receives and decrypt content
