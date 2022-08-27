def generate_message_to_logger(msg, log_level):
    return f"{msg},{log_level}"


def generate_message_to_discord_messenger(msg, channel, info):
    return f"{msg},{channel},{info}"


def generate_message_to_server(server_command, worker, worker_command=None, msg=None):
    if server_command == "REGISTER":
        return f"{server_command}:{worker}"
    if server_command == "POST":
        return f"{server_command}:{worker},{worker_command},{msg}"
    if server_command == "GET":
        return f"{server_command}:{worker},{worker_command}"


class ClientIf:
    def connect_to_server(self):
        pass

    def send_message(self, message):
        pass

    def recv_message(self):
        pass

    def register_features_to_server(self):
        pass

    def close(self):
        pass
