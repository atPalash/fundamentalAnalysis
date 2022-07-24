import traceback

from ai.lstm.lstm_model import LstmModel
from utility.logger import Logger, LogLevel
from utility.discordBot.discord_messenger import DiscordMessenger
from conf import conf_editor
from ai.discord_routes import DiscordRoutes
import numpy


class Orchestrator:
    def __init__(self):
        self.config = conf_editor.read()
        self.name = "ai orchestrator"
        lstm_model = LstmModel("lstm", config=self.config, epoch=20, debug=False, debug_count=2)
        self.models = {"lstm": lstm_model}

        # First initialise discord messenger with general channel
        DiscordMessenger.initialise(self.config['discord_config']['messenger']['webhook'])
        self.discord_routes = DiscordRoutes(name="query_routes", listener_config=self.config['discord_config']['listener'],
                                            user_config=self.config['user_config'], parent=self)

    def build(self, model=""):
        for name, model in self.models.items():
            try:
                msg = f"Building model for {name}"
                Logger.log(msg=msg, log_level=LogLevel.Info)
                DiscordMessenger.send_message(channel="general", msg=msg, title=f"Build {name}")

                model.build_model()
            except Exception as e:
                msg = f"Exception occurred while building model {model}"
                Logger.log(msg=msg + f"\n{traceback.format_exc()}", log_level=LogLevel.Error)
                DiscordMessenger.send_message(channel="general", msg=msg, title=f"{type(e).__name__}")

    def predict(self, model: str, stock: str):
        try:
            model = self.models[model]
            stock_prediction, trend = model.predict_with_model(stock=stock)

            return stock_prediction[-1][0], trend
        except Exception as e:
            msg = f"Exception occurred while predicting with model {model}"
            Logger.log(msg=msg + f"\n{traceback.format_exc()}", log_level=LogLevel.Error)
            DiscordMessenger.send_message(channel="general", msg=msg, title=f"{type(e).__name__}")