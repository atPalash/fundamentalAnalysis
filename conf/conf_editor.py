from pathlib import Path

from utility.reader import read_config

conf_folder = Path(r"D:\pythonProjects\fundamentalAnalysis\conf")


def read():
    user_config = conf_folder / "user.yml"
    user_config = read_config(user_config.resolve(strict=True).as_posix())
    indicator_config = conf_folder / "indicator.yml"
    indicator_config = read_config(indicator_config.resolve(strict=True).as_posix())
    selected_stocks_config = conf_folder / "selected_stocks.yml"
    selected_stocks_config = read_config(selected_stocks_config.resolve(strict=True).as_posix())
    discord_config = conf_folder / "discord.yml"
    discord_config = read_config(discord_config.resolve(strict=True).as_posix())
    port_config = conf_folder / "client_port.yml"
    port_config = read_config(port_config.resolve(strict=True).as_posix())
    return {"user_config": user_config,
            "indicator_config": indicator_config,
            "selected_stocks_config": selected_stocks_config,
            "discord_config": discord_config,
            "port_config": port_config,
            }
