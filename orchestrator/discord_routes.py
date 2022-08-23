from utility.discordBot.discord_listener import DiscordListener
import orchestrator.route_methods as route
from utility.aggregator import singletons


class DiscordRoutes:
    def __init__(self, name: str, listener_config: dict, user_config: dict):
        self.name = name
        self.route_methods = route.route_methods
        route.set_configs(user_config)
        self.__add_route()

    def __add_route(self):
        if len(self.route_methods.keys()) == 0:
            raise Exception("No routes defined reinitialise again")
        for k, v in self.route_methods.items():
            singletons['discord_listener'].add_route(k, v)

    def stop(self):
        # singletons['discord_listener'].stop()
        self.route_methods = {}

    @staticmethod
    def set_indicator_results(indicator_results: dict):
        route.set_indicator_results(indicator_results)