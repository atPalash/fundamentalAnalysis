from clientIf import ClientIf
from conf.conf_editor import read
import socket


class LoggerTest(ClientIf):
    def __init__(self, host, port, configuration):
        self.name = "Logger test client"
        self.configuration = configuration
        self.host = host
        self.port = port
        self.client_socket = None

        self.connect_to_server()
        msg = f"CALL:discord_messenger,general,hello,info"
        self.send_message(msg)

        while True:
            self.recv_message()

    def connect_to_server(self):
        self.client_socket = socket.socket()  # instantiate
        self.client_socket.connect((self.host, self.port))  # connect to the server

    def send_message(self, message):
        self.client_socket.send(message.encode())  # send message

    def recv_message(self):
        data = self.client_socket.recv(1024).decode()  # receive response
        print(data)

    def register_features_to_server(self):
        pass

    def close(self):
        self.client_socket.close()


if __name__ == '__main__':
    conf = read()
    tester = LoggerTest(host=socket.gethostname(), port=conf['port_config']['server'], configuration=conf)
