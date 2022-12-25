# https://gist.github.com/BenKnisley/5647884

import socket, time


def Tcp_connect(HostIp, Port):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HostIp, Port))
    return


def Tcp_Write(D):
    s.send(D.encode())
    return


def Tcp_Read():
    return s.recv(1024).decode()


def Tcp_Close():
    s.close()
    return


def handleReceiver():
    Tcp_connect("127.0.0.1", 12345)
    Tcp_Write("hello sender")
    print(Tcp_Read())
    time.sleep(1)
    Tcp_Write("hello sender again")
    print(Tcp_Read())
    Tcp_Close()
