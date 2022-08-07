import discord
from typing import List
from stockNews.google_news_handler import GoogleNewsHandler

user_config = {}
indicator_results = {}


def set_configs(config: dict):
    global user_config
    user_config = config


def set_indicator_results(results: dict):
    global indicator_results
    indicator_results = results


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
        method = route_methods.get(args[0])
        if method is not None:
            res = f"{method.__name__}\n{method.__doc__}"
        else:
            res = "This method is not available, check all methods available commands: all"
    return res


def headlines(*args):
    """
    Send default number of news headlines when only ticker is passed as argument. For news count and days user must
    define both. Also raise error on calling without ticker or valid ticker. User can click on the links to check the
    detailed article.

    Parameters
    ----------
    args :
        ticker: string, mandatory
            User sends one ticker.
        days: past number of days to search for news
        count: number of news result to show

    Returns
    ---------
        discord embedded message with description set to clickable headlines to detailed articles

    Example
    ---------
    headlines: adani,10,30 -> shows 30 result from last 10 days
    headlines: adani -> shows result from last default days and count
    """
    try:
        user_args = __clean_user_args(args[0].split(","))
        arg_count = len(user_args)
        res = ""
        if arg_count == 3:
            ticker = str(user_args[0])
            days = int(user_args[1])
            count = int(user_args[2])
            head_lines = GoogleNewsHandler.get_headlines(ticker=ticker, past_days=days, max_news_count=count)

        elif arg_count >= 1:
            ticker = str(user_args[0])
            head_lines = GoogleNewsHandler.get_headlines(ticker=ticker,
                                                         past_days=user_config['google_news']['past_days'],
                                                         max_news_count=user_config['google_news']['max_news_count'])
        else:
            raise Exception("ticker not defined")

        news_count = 0
        for news in head_lines:
            news_count += 1
            res += f"[{news_count}. {news.title}]({news.link}) \n "

        return res
    except Exception as e:
        raise


def sentiment(*args):
    """
    Judge sentiment for the stock ticker provided.

    Parameters
    ----------
    args : list[string], mandatory
        User sends ticker name/names as a list separated by ","

    Returns
    ---------
        discord embedded message with description set to sentiment

    Example
    ---------
    sentiment: adani,tcs -> get sentiment of adani, tcs from last headlines news collected by calling headlines.
    sentiment: adani -> get sentiment of adani default news count
    """
    tickers = __clean_user_args(args[0].split(","))
    if tickers[-1].isdigit():
        tickers.pop()

    ticker_sentiments = ""
    for ticker in tickers:
        senti = GoogleNewsHandler.get_sentiment(ticker=ticker)
        ticker_sentiments += f"{ticker}: {senti}\n"
    return ticker_sentiments


def indicator(*args):
    global indicator_results
    query = __clean_user_args(args[0].split(","))

    res = ""
    stocks = query[1:]
    for stk in stocks:
        stk_nse = f"{stk.upper()}.NS"
        res += f"{stk}:{indicator_results[query[0]][stk_nse]}"
    return res


def stock(*args):
    global indicator_results
    query = __clean_user_args(args[0].split(","))
    stk = query[0]
    res = ""
    indicators = query[1:]
    for ind in indicators:
        stk_nse = f"{stk.upper()}.NS"
        res += f"{stk}:{indicator_results[ind][stk_nse]}"
    return res


def __clean_user_args(data: List[str]):
    ret = [x.strip() for x in data]
    return ret


route_methods = dict(commands=commands, headlines=headlines, sentiment=sentiment, indicator=indicator, stock=stock)
