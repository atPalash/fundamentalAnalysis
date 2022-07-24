from utility.discordBot.discord_listener import DiscordListener

from typing import List


class DiscordRoutes:
    def __init__(self, name: str, listener_config: dict, user_config: dict, parent):
        self.orchestrator = parent
        self.name = name
        self.route_methods = {}
        self.set_route_methods()
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

    def set_route_methods(self):

        def commands(*args):
            """
            List all methods which can be queried from Discord.
            e.g.:
            commands: all -> list all command api.
            commands: <command> -> shows api for specified command.
            Keyword arguments:
            data -- numbers separated by ","
            """
            res = ""
            if args[0] == "all":
                for method, func in self.route_methods.items():
                    res += f"{method}:{func.__doc__}\n"
            else:
                method = self.route_methods.get(args[0])
                if method is not None:
                    res = f"{method.__name__}\n{method.__doc__}"
                else:
                    res = "This method is not available, check all methods available commands: all"
            return res

        def predict(*args):
            """
            Predict future price based on ai trained models.

            Parameters
            ----------
            args : list[string], mandatory
                User sends ticker name/names as a list separated by ","

            Returns
            ---------
                discord embedded message with description set to prediction for each stock

            Example
            ---------
            predict: adani,tcs -> get sentiment of adani, tcs
            predict: adani -> get sentiment of adani
            """
            tickers = __clean_user_args(args[0].split(","))
            if tickers[-1].isdigit():
                tickers.pop()

            ticker_predictions = ""
            for ticker in tickers:
                prediction, trend = self.orchestrator.predict(model="lstm", stock=ticker)
                ticker_predictions += f"{ticker}: {prediction}, trend: {trend}\n"
            return ticker_predictions

        def __clean_user_args(data: List[str]):
            ret = [x.strip() for x in data]
            return ret

        self.route_methods = dict(commands=commands, predict=predict)



