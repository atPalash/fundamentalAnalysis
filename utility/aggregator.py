from utility.discordBot.discord_listener import DiscordListener
from utility.discordBot.discord_messenger import DiscordMessenger
from utility.logger import Logger, LogLevel
from conf.conf_editor import read

configuration = read()
__discord_listener = DiscordListener(configuration['discord_config'])
__discord_messenger = DiscordMessenger(configuration['discord_config']['messenger']['webhook'])
__logger = Logger()

singletons = {
    'discord_listener': __discord_listener,
    'discord_messenger': __discord_messenger,
    'logger': __logger
}