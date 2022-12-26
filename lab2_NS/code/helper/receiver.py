# https://gist.github.com/BenKnisley/5647884

import socket, time


def Tcp_connect(HostIp, Port):
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
    s.connect((HostIp, Port))
    print("Connecting to machine with ip: " + str(HostIp) + " and port: " + str(Port))
    return


def Tcp_Write(D):
    s.send(D.encode())
    return


def Tcp_Read():
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


def Tcp_Close():
    s.close()
    return


def handleReceiver(hostIP, port, data):
    Tcp_connect(hostIP, port)
    print(data)
    Tcp_Write(data)
    # response = Tcp_Read()
    Tcp_Close()
    # return response


# handleReceiver()
