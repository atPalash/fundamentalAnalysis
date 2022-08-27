import orchestrator.route_methods as route
from utility.aggregator import get_singletons

# TDOD update this
class DiscordRoutes:
    def __init__(self, name: str, configuration: dict):
        self.name = name
        self.route_methods = route.route_methods
        route.set_configs(configuration['user_config'])
        self.__add_route()
        self.listener = get_singletons(configuration=configuration)['discord_listener']

    def __add_route(self):
        if len(self.route_methods.keys()) == 0:
            raise Exception("No routes defined reinitialise again")
        for k, v in self.route_methods.items():
            self.listener.add_route(k, v)

    def stop(self):
        # singletons['discord_listener'].stop()
        self.route_methods = {}

    @staticmethod
    def set_indicator_results(indicator_results: dict):
        route.set_indicator_results(indicator_results)