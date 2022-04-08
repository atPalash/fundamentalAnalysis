import threading
from enum import Enum
import discord

from utility.reader import read_config


class DiscordBotChannel(Enum):
    GENERAL = 1
    SELL = 2
    BUY = 3
    QUERY = 4


class DiscordBot:
    """
    Add webhook to discord to send message on channel
    """
    _general_webhook = None
    _buy_webhook = None
    _sell_webhook = None
    _is_bot_available = False
    _discord_config = None

    @staticmethod
    def send_message(channel: DiscordBotChannel, msg):
        if DiscordBot._general_webhook is None:
            msg = "Initialise Discord bot and send message"
            print(msg)
            raise Exception(msg)
        if channel == DiscordBotChannel.BUY:
            DiscordBot._buy_webhook.send(msg)
        elif channel == DiscordBotChannel.SELL:
            DiscordBot._sell_webhook.send(msg)
        else:
            DiscordBot._general_webhook.send(msg)

    @staticmethod
    def initialise(config):
        if DiscordBot._general_webhook is None:
            DiscordBot._discord_config = read_config(config)
            general_url = DiscordBot._discord_config['webhook']['general']
            buy_url = DiscordBot._discord_config['webhook']['buy']
            sell_url = DiscordBot._discord_config['webhook']['sell']

            DiscordBot._general_webhook = discord.Webhook.from_url(
                general_url, adapter=discord.RequestsWebhookAdapter())
            DiscordBot._sell_webhook = discord.Webhook.from_url(
                sell_url, adapter=discord.RequestsWebhookAdapter())
            DiscordBot._buy_webhook = discord.Webhook.from_url(
                buy_url, adapter=discord.RequestsWebhookAdapter())

            discord_listener = DiscordListener()
            discord_listener.start()


class DiscordListener(threading.Thread, DiscordBot):
    """
    Initialise the Discord bot before initialising the listener for it
    """
    _client = None

    def __init__(self):
        super().__init__()
        if DiscordListener._client is None:
            DiscordListener._client = discord.Client()

            @DiscordListener._client.event
            async def on_ready():
                DiscordBot._is_bot_available = True

            @DiscordListener._client.event
            async def on_message(message):
                if not DiscordBot._is_bot_available:
                    return

                if message.author == DiscordListener._client.user:
                    return

                if message.channel.name == "query":
                    await message.channel.send("lets do some query")

        else:
            raise Exception("Must not create multiple Discord listener")

    def run(self):
        DiscordListener._client.run(DiscordBot._discord_config['bot']['token'])
