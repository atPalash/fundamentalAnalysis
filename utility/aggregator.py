from utility.discordBot.discord_listener import DiscordListener
from utility.discordBot.discord_messenger import DiscordMessenger
from utility.logger import Logger, LogLevel
from conf.conf_editor import read

from multiprocessing.connection import Listener

configuration = read()
__discord_listener = DiscordListener(configuration['discord_config'])
__discord_messenger = DiscordMessenger(configuration['discord_config']['messenger']['webhook'])
__logger = Logger()

singletons = {
    'discord_listener': __discord_listener,
    'discord_messenger': __discord_messenger,
    'logger': __logger
}

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'
listener = Listener(address, authkey=b'secret password')
conn = listener.accept()
print ('connection accepted from', listener.last_accepted)
while True:
    msg = conn.recv()
    # do something with msg
    if msg == 'close':
        conn.close()
        break
    elif msg == 'get_singletons':
        conn.send(singletons)

        
listener.close()