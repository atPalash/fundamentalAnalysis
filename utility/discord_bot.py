from enum import Enum
from discord import Webhook, RequestsWebhookAdapter


class DiscordBotChannel(Enum):
    GENERAL = 1
    SELL = 2
    BUY = 3


class DiscordBot:
    _general_url = "https://discord.com/api/webhooks/960272984977854535/YZw8kDtbSOyC1epj-S2_VaoE61z1GQg1Z-__53Ck-eD7a-pnNSEJwNWZ7dhClvHVhKga"
    _sell_url = "https://discord.com/api/webhooks/960273089256644658/WtzbdclvQCOkYrcgjsAbVCsuTnbcIl0mfeoIPv6-io0b92mJRQuhM1AYm6_OKfrqiBMP"
    _buy_url = "https://discord.com/api/webhooks/960273172610023425/Sh7QXscdduMDnFgsNLc9OIE0op83mG_EiUeNwGdkDcPMdaRDqhobSxbnpyMy4CHWTZ-q"

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

