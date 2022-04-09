from utility.discordBot.discord_listener import DiscordListener
from orchestrator.route_methods import route_methods


class DiscordRoutes:
    def __init__(self, name: str, listener_config: dict):
        self.name = name
        self.route_methods = route_methods
        # listener only available for query channel
        DiscordListener.initialise(channel_name="query", token=listener_config['bot']['token'])
        self.__add_route()
        DiscordListener.run()

    def __add_route(self):
        if len(self.route_methods.keys()) == 0:
            raise Exception("No routes defined reinitialise again")
        for k, v in self.route_methods.items():
            DiscordListener.add_route(k, v)

    def stop(self):
        DiscordListener.stop()
        self.route_methods = {}