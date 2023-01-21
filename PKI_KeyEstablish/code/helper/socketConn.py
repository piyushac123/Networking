# https://gist.github.com/BenKnisley/5647884

import socket, time


def Tcp_server_connect(numofclientwait, port):
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
    s2.bind(("", port))
    print("socket binded to %s" % (port))
    s2.listen(numofclientwait)
    print("socket is listening")
    return s2


def Tcp_client_connect(hostIp, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
    s.connect((hostIp, port))
    print("Connecting to machine with ip: " + str(hostIp) + " and port: " + str(port))
    return s


def Tcp_server_next(s2):
    return s2.accept()[0]


def Tcp_Write(s, D):
    s.send(D.encode())
    return


def Tcp_Read(s):
    result = ""
    while True:
        cnt = 0
        while (tmp := s.recv(1).decode()) and (tmp == "*"):
            cnt += 1
            result += tmp
        if cnt == 5:
            result = result[:-5]
            break
        result += tmp
    return result


def Tcp_Close(s):
    s.close()
    return
