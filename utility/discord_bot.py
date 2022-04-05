from enum import Enum
from discord import Webhook, RequestsWebhookAdapter

from utility.reader import read_config


class DiscordBotChannel(Enum):
    GENERAL = 1
    SELL = 2
    BUY = 3

'''
Add webhook to discord to send message on channel
'''
class DiscordBot:
    _general_webhook = None
    _buy_webhook = None
    _sell_webhook = None

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
            
            DiscordBot._general_webhook = Webhook.from_url(general_url, adapter=RequestsWebhookAdapter())
            DiscordBot._sell_webhook = Webhook.from_url(sell_url, adapter=RequestsWebhookAdapter())
            DiscordBot._buy_webhook = Webhook.from_url(buy_url, adapter=RequestsWebhookAdapter())

