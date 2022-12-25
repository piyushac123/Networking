# https://gist.github.com/BenKnisley/5647884

import socket, time


def Tcp_server_wait(numofclientwait, port):
    global s2
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s2.bind(("", port))
    s2.listen(numofclientwait)


def Tcp_server_next():
    global s
    s = s2.accept()[0]


def Tcp_Write(D):
    s.send(D.encode())
    return


def Tcp_Read():
    return s.recv(1024).decode()


def Tcp_Close():
    s.close()
    return


def handleSender():
    Tcp_server_wait(5, 12345)
    Tcp_server_next()
    print(Tcp_Read())
    time.sleep(1)
    Tcp_Write("hi receiver")
    print(Tcp_Read())
    time.sleep(1)
    Tcp_Write("hi receiver again")
    Tcp_Close()
