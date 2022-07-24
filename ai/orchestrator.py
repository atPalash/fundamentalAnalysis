import traceback

from ai.lstm.lstm_model import LstmModel
from utility.logger import Logger, LogLevel
from utility.discordBot.discord_messenger import DiscordMessenger
from conf import conf_editor


class Orchestrator:
    def __init__(self):
        self.name = "ai orchestrator"
        lstm_model = LstmModel("lstm", config=conf_editor.read(), debug=True, debug_count=2)
        self.models = {"lstm": lstm_model}

    def build(self, model=""):
        for _, model in self.models.items():
            try:
                model.build_model()
            except Exception as e:
                msg = f"Exception occurred while building model {model}"
                Logger.log(msg=msg + f"\n{traceback.format_exc()}", log_level=LogLevel.Error)
                DiscordMessenger.send_message(channel="general", msg=msg, title=f"{type(e).__name__}")

    def predict(self, stock: str):
        predictions = {}
        for _, model in self.models.items():
            try:
                stock_prediction = model.predict_with_model()
                predictions[stock] = stock_prediction[-1]
            except Exception as e:
                msg = f"Exception occurred while predicting with model {model}"
                Logger.log(msg=msg + f"\n{traceback.format_exc()}", log_level=LogLevel.Error)
                DiscordMessenger.send_message(channel="general", msg=msg, title=f"{type(e).__name__}")
