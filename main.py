from orchestrator.orchestrator import Orchestrator
from utility.discord_bot import DiscordBot
from utility.logger import Logger, LogLevel

if __name__ == "__main__":
    Logger.log("STARTING ANALYSIS", LogLevel.Info)
    user_config = "/home/pi/Dev/fundamentalAnalysis/conf/user.yml"
    indicator_config = "/home/pi/Dev/fundamentalAnalysis/conf/indicator.yml"
    selected_stocks_config = "/home/pi/Dev/fundamentalAnalysis/conf/selected_stocks.yml"
    discord_config = "/home/pi/Dev/fundamentalAnalysis/conf/discord.yml"

    orchestrator = Orchestrator(user_config=user_config, indicator_config=indicator_config,
                                selected_stocks_config=selected_stocks_config)
    DiscordBot.initialise(discord_config)
    orchestrator.run()