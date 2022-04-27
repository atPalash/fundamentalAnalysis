import discord

from stockNews.google_news_handler import GoogleNewsHandler

EMBEDDED_MSG_SIZE = 2096


def commands(*args):
    """
    List all methods which can be queried from Discord.
    e.g.:
    commands: all -> list all command api.
    commands: <command> -> shows api for specified command.
    Keyword arguments:
    data -- numbers separated by ","
    """
    res = ""
    if args[0] == "all":
        for method, func in route_methods.items():
            res += f"{method}:{func.__doc__}\n"
    else:
        if route_methods.get(args[0]) is not None:
            res = route_methods[args[0]].__doc__
        else:
            res = "This method is not available, check all methods available commands: all"
    return __convert_to_chunks('commands', res)


def headlines(*args):
    """
    Send default number of news headlines when only ticker is passed as argument. For news count and days user must
    define both. Also raise error on calling without ticker or valid ticker. User can click on the links to check the
    detailed article.
    """
    try:
        user_args = args[0].split(",")
        arg_count = len(user_args)
        res = ""
        if arg_count == 3:
            ticker = str(user_args[0])
            days = int(user_args[1])
            count = int(user_args[2])
            headlines = GoogleNewsHandler.get_headlines(ticker=ticker, past_days=days, max_news_count=count)

        elif arg_count >= 1:
            ticker = str(user_args[0])
            headlines = GoogleNewsHandler.get_headlines(ticker=ticker)
        else:
            raise Exception("ticker not defined")

        for index, row in headlines.iterrows():
            res += f"[{index}. {row['title']}](https://{row['link']}) \n "

        return __convert_to_chunks("headlines", res)
    except Exception as e:
        raise


def __convert_to_chunks(title: str, msg: str):
    """
    Converts the message sent in chunks for proper discord message send.
    """
    embeds = []

    if len(msg) < EMBEDDED_MSG_SIZE:
        embed = __create_embed(title=title, msg=msg)
        embeds.append(embed)
    else:
        msgs = msg.split('\n')

        des = ""
        for message in msgs:
            if len(des) < EMBEDDED_MSG_SIZE:
                des += message + '\n'
            else:
                embed = __create_embed(title=title, msg=des)
                embeds.append(embed)
                des = ""

        if des != "":
            embed = __create_embed(title=title, msg=des)
            embeds.append(embed)

    return embeds


def __create_embed(title: str, msg: str):
    embed = discord.Embed()
    embed.title = title
    embed.description = msg
    return embed


route_methods = dict(commands=commands, headlines=headlines)
