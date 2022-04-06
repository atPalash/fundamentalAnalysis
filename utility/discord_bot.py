from enum import Enum
import discord
from discord.ext import commands

from utility.reader import read_config


class DiscordBotChannel(Enum):
    GENERAL = 1
    SELL = 2
    BUY = 3
    QUERY = 4


'''
Add webhook to discord to send message on channel
'''
class DiscordBot:
    _general_webhook = None
    _buy_webhook = None
    _sell_webhook = None
    _is_bot_available = False

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
            discord_config = read_config(config)
            general_url = discord_config['webhook']['general']
            buy_url = discord_config['webhook']['buy']
            sell_url = discord_config['webhook']['sell']

            DiscordBot._general_webhook = discord.Webhook.from_url(
                general_url, adapter=discord.RequestsWebhookAdapter())
            DiscordBot._sell_webhook = discord.Webhook.from_url(
                sell_url, adapter=discord.RequestsWebhookAdapter())
            DiscordBot._buy_webhook = discord.Webhook.from_url(
                buy_url, adapter=discord.RequestsWebhookAdapter())

            # stops execution check here
            # client = discord.Client()

            # @client.event
            # async def on_ready():
            #     DiscordBot._is_bot_available = True

            # @client.event
            # async def on_message(message):
            #     if not DiscordBot._is_bot_available:
            #         DiscordBot.send_message("Bot unavailable", DiscordBotChannel.GENERAL)
            #         return
                
            #     if message.author == client.user:
            #         return

            #     if message.channel.name == "query":
            #         await message.channel.send("lets do some query")
            #     else:
            #         await message.channel.send("Use query channel")

            # client.run(discord_config['bot']['token'])
    

if __name__ == "__main__":
    discord_config = "/home/pi/Dev/fundamentalAnalysis/conf/discord.yml"
    DiscordBot.initialise(discord_config)
    DiscordBot.send_message("hello", DiscordBotChannel.GENERAL)
