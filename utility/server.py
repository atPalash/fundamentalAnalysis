import traceback

import requests
from flask import Flask, request, jsonify

from conf.conf_editor import read
from request import Request, ErrorCode
from serverIf import ServerIf
from utility.discordBot.discord_listener import DiscordListener
from utility.discordBot.discord_messenger import DiscordMessenger
from utility.logger import LoggerFactory

master_server_url = "http://127.0.0.1:8000/"
this_server_url = "http://127.0.0.1:8001/"


class Server(ServerIf):
    def __init__(self, configuration):
        self.name = "Utility server"
        self.configuration = configuration
        self.services = {}
        self.routes = {}
        self.log_folder = r"D:\pythonProjects\fundamentalAnalysis\logs"

        self.discord_messenger = DiscordMessenger(self.configuration['discord_config']['messenger']['webhook'])
        self.logger = LoggerFactory.get_logger(log_folder=self.log_folder)

        self.discord_listener = DiscordListener(discord_config=self.configuration['discord_config'],
                                                discord_messenger=self.discord_messenger)

        # self.add_service("discord_listener", self.discord_listener)
        self.add_service("discord_messenger", self.discord_messenger)
        self.add_service("logger", self.logger)

        self.register_routes_to_app()

    def get_services(self):
        return self.routes

    def add_service(self, service, obj):
        self.services[service] = obj
        self.routes[service] = this_server_url

    def register_routes_to_app(self):
        try:
            Request.post(master_server_url + "/route", data=self.routes)
        except Exception:
            raise


app = Flask(__name__)
server = Server(read())


@app.get("/service")
def get_service():
    global server
    return server.routes


@app.post("/service")
def call_service():
    global server
    if request.is_json:
        err = ""
        response = ""
        error_code = ErrorCode.OK
        try:
            routes = request.get_json()

            key = list(routes.keys())[0]
            if key == "logger":
                server.logger.info(msg=routes[key]['msg'])
                response = "LOGGED"
            elif key == "discord_messenger":
                server.discord_messenger.send_message(channel=routes[key]['channel'],
                                                      msg=routes[key]['msg'],
                                                      title=routes[key]['title'])
                response = "SENT DISCORD MESSAGE"
            return Request.make_response(error_code=error_code, err_message=err, body=response)
        except Exception as e:
            error_code = ErrorCode.Critical
            err = f"{e.args}"
            server.logger.error(e.args)
            return Request.make_response(error_code=error_code, err_message=err, body=traceback.format_exc())
    err = f"request must be json"
    return Request.make_response(error_code=ErrorCode.Critical, err_message=err), 415


if __name__ == '__main__':
    app.run(host="localhost", port=8001)
