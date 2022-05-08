from utility.discordBot.discord_listener import DiscordListener
import orchestrator.route_methods as route


class DiscordRoutes:
    def __init__(self, name: str, listener_config: dict, user_config: dict):
        self.name = name
        self.route_methods = route.route_methods
        route.set_configs(user_config)
        # listener only available for query channel
        DiscordListener.initialise(listener_config=listener_config)
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