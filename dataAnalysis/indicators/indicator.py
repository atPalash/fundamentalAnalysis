import traceback
from abc import abstractmethod
from utility.discordBot.discord_messenger import DiscordMessenger
from utility.logger import Logger, LogLevel


class Indicator:
    """
    This is the interface class which is implemented by the individual child class.
    """

    def __init__(self, config, data, name):
        self.config = config
        self.data = data
        self.name = name
        self.results = {}

    @abstractmethod
    def do_analysis(self, selected_stocks: list):
        pass

    def set_result(self, result: dict):
        """
        set the result dict. As shown in the following format.
        {
            indicator1: {
                stock1 : value1
                stock2 : value2
                .
                .
                .
            },
            indicator2: {
                stock1 : value1
                stock2 : value2
                .
                .
                .
            },
            .
            .
            .
        }
        """
        self.results = result

    def get_result(self):
        return self.results

    # Set data on which the indicator calculation is to be done
    @abstractmethod
    def __get_result(self, col_data):
        pass

    def log_message(self, log_msg: str, log_level: LogLevel, discord_msg: str, discord_channel: str):
        """
        Log results and exceptions in indicator
        """
        Logger.log(msg=log_msg, log_level=log_level)
        DiscordMessenger.send_message(channel=discord_channel, msg=discord_msg, title=self.name)
