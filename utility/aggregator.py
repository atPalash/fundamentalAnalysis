import clientIf
from clientIf import ClientIf
from conf.conf_editor import read
from utility.discordBot.discord_listener import DiscordListener
from utility.discordBot.discord_messenger import DiscordMessenger
from utility.logger import Logger, LogLevel
import socket


class Utility(ClientIf):
    def __init__(self, host, port, configuration):
        self.name = "Utility client"
        self.configuration = configuration
        self.host = host
        self.port = port
        self.client_socket = None

        self.discord_listener = DiscordListener(self.configuration['discord_config'])
        self.discord_messenger = DiscordMessenger(self.configuration['discord_config']['messenger']['webhook'])
        self.logger = Logger()

        self.connect_to_server()
        self.register_features_to_server()

        while True:
            self.recv_message()

    def connect_to_server(self):
        self.client_socket = socket.socket()  # instantiate
        self.client_socket.connect((self.host, self.port))  # connect to the server

    def send_message(self, message):
        self.client_socket.send(message.encode())  # send message

    def recv_message(self):
        data = self.client_socket.recv(1024).decode().strip().split(',') # receive response

        try:
            worker = data[0]
            if worker == 'logger':
                if len(data) > 2:
                    self.logger.log(data[1], log_level=data[2])
            elif worker == 'discord_messenger':
                self.discord_messenger.send_message(channel=data[1], msg=data[2], title=data[3])
        except Exception as e:
            self.logger.log(msg=data, log_level=LogLevel.Error)
            self.discord_messenger.send_message(channel="general", msg=data + "\n" + e.args, title="Error")

    def register_features_to_server(self):
        for feature in self.get_singletons().keys():
            message = clientIf.generate_message_to_server("REGISTER", worker=feature)
            self.send_message(message)

    def close(self):
        self.client_socket.close()

    def get_singletons(self):
        return {
                'discord_listener': self.discord_listener,
                'discord_messenger': self.discord_messenger,
                'logger': self.logger
            }


if __name__ == '__main__':
    conf = read()
    utils = Utility(host=socket.gethostname(), port=conf['port_config']['server'], configuration=conf)
