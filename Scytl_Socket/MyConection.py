import socket

class MyConnection(object):
    def __init__(self, host, port):
        self.MySocket = socket.create_connection((host, port), socket._GLOBAL_DEFAULT_TIMEOUT)

    def get_msg(self):
        msg = ""
        while True:
            msg = self.MySocket.recv(7).decode('latin_1')
        if ord(msg[len(msg)-1]) == 0x21:
            return msg

    def send_msg(self, msg):
        self.MySocket.sendall(msg.encode())

    def close_socket(self):
        self.MySocket.close()
