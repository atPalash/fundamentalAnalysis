from orchestrator.orchestrator import Orchestrator
from utility.discord_bot import DiscordBot
from utility.logger import Logger, LogLevel
from pathlib import Path

if __name__ == "__main__":
    Logger.log("STARTING ANALYSIS", LogLevel.Info)
    conf_folder = Path("conf")
    user_config = conf_folder/"user.yml"
    user_config = user_config.resolve(strict=True).as_posix()
    indicator_config = conf_folder/"indicator.yml"
    indicator_config = indicator_config.resolve(strict=True).as_posix()
    selected_stocks_config = conf_folder/"selected_stocks.yml"
    selected_stocks_config = selected_stocks_config.resolve(strict=True).as_posix()
    discord_config = conf_folder/"discord.yml"
    discord_config = discord_config.resolve(strict=True).as_posix()

    orchestrator = Orchestrator(user_config=user_config, indicator_config=indicator_config,
                                selected_stocks_config=selected_stocks_config)
    DiscordBot.initialise(discord_config)
    orchestrator.run()