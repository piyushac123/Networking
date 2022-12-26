# https://gist.github.com/BenKnisley/5647884

import socket, time


def Tcp_server_wait(numofclientwait, port):
    global s2
    s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
    s2.bind(("", port))
    print("socket binded to %s" % (port))
    s2.listen(numofclientwait)
    print("socket is listening")


def Tcp_server_next():
    global s
    s = s2.accept()[0]


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


def handleSender(port):
    Tcp_server_wait(5, port)
    Tcp_server_next()
    print(Tcp_Read())
    Tcp_Close()


# handleSender()
