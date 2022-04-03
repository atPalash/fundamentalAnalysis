from enum import Enum
from discord import Webhook, RequestsWebhookAdapter


class DiscordBotChannel(Enum):
    GENERAL = 1
    SELL = 2
    BUY = 3


class DiscordBot:
    _general_url = "https://discord.com/api/webhooks/960081046647492618/LWhY4ftN_RsMrtoYMOPFk1sScW0YC_zMY7vuHO0OmtJrm6oYol8BHWNSXBmTjU3xxI-e"
    _sell_url = "https://discord.com/api/webhooks/960081289690644550/QcXzoKKiOQiVbfDLD5SggQSWHp8HXudorYEINcwEduWrGO3-hsjob5JNF4svJo7szmrk"
    _buy_url = "https://discord.com/api/webhooks/960081364672192542/oYJz6c8yy5EqzFNeiupGTOWNBefRYYdln8SfOvm9jN-g33E9gI-lzxh0-Htoq6jGXsqI"

    _general_webhook = None
    _buy_webhook = None
    _sell_webhook = None

    @staticmethod
    def send_message(channel: DiscordBotChannel, msg):
        DiscordBot.__initialise()
        if channel == DiscordBotChannel.BUY:
            DiscordBot._buy_webhook.send(msg)
        elif channel == DiscordBotChannel.SELL:
            DiscordBot._sell_webhook.send(msg)
        else:
            DiscordBot._general_webhook.send(msg)

    @staticmethod
    def __initialise():
        if DiscordBot._general_webhook is None:
            DiscordBot._general_webhook = Webhook.from_url(DiscordBot._general_url, adapter=RequestsWebhookAdapter())
            DiscordBot._sell_webhook = Webhook.from_url(DiscordBot._sell_url, adapter=RequestsWebhookAdapter())
            DiscordBot._buy_webhook = Webhook.from_url(DiscordBot._buy_url, adapter=RequestsWebhookAdapter())

