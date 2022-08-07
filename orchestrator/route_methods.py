import discord
from typing import List

import pandas
from dataFetch.yfinance_live_data import YFinanceLiveData
from stockNews.google_news_handler import GoogleNewsHandler
from conf import conf_editor

user_config = {}
indicator_results = {}

# TODO remove this
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


def highlow52w(*args):
    """
    Inform user of selected stocks currently at their 52 weeks high and low.

    Parameters
    ----------
    args :
        sel - shows only selected stocks
        OR
        all - checks all NSE traded stocks and lists them.

        band_range - percentage of range for high and low.
    Returns
    ---------
        discord embedded message with list of stocks at 52 week high or low. 

    Example
    ---------
    highlow52W: sel, 10 -> shows list of selected stocks within  52 high / low.
    highlow52W: all, 10 -> shows list of all nse stocks at 52 high / low.
    """ 
    try:
        configuration = conf_editor.read()
        query = __clean_user_args(args[0].split(","))
        selected_stocks = []
        if query[0] == 'sel':
            stocks = configuration['selected_stocks_config']['to_buy'] + configuration['selected_stocks_config']['to_sell']
            selected_stocks = [stock + ".NS" for stock in stocks]
        elif query[0] == 'all':
            all_nse_stocks = pandas.read_csv('conf/ind_NseList.csv')['SYMBOL']
            selected_stocks = [stock + ".NS" for stock in all_nse_stocks]
        else:
            return "use sel or all as argument"

        if len(query) > 1 and query[1].isdigit():
            band_percentage = int(query[1])
        else:
            band_percentage = configuration['user_config']['band_percentage']

        high52w = {}
        low52w = {}
        batch_size = 100
        batches = [selected_stocks[i:i + batch_size] for i in range(0, len(selected_stocks), batch_size)]
        # call in batches
        for batch in batches:
            # fetch 52 week data till current
            stock_config = {
                'tickers': batch,
                'interval': configuration['user_config']['yf_interval'],
                'period': '1y'
            }
            yfinance = YFinanceLiveData(stock_config)
            data = yfinance.get_tickers_historical_data()

            for stk in batch:
                try:
                    # Check if current price is greater than the highest 52 week price range
                    high52 = data['High'][stk].max()
                    if data['High'][stk][-1] >= high52 - high52 * band_percentage/100:
                        high52w[stk] = high52

                    # Check if current price is lower than the lower 52 week price range
                    low52 = data['Low'][stk].min()
                    if data['Low'][stk][-1] <= low52 + low52 * band_percentage / 100:
                        low52w[stk] = low52
                except Exception as e:
                    print(f"{stk} exception: {e.args[0]}")

        res = "*** 52W high ***\n"
        count = 1
        for stk, val in high52w.items():
            res += f"{count}. {stk}: {val} \n "
            count += 1

        res += "\n*** 52W low ***\n"
        count = 1
        for stk, val in low52w.items():
            res += f"{count}. {stk}: {val} \n "
            count += 1

        return res
    except Exception as e:
        print(e)


def __clean_user_args(data: List[str]):
    ret = [x.strip() for x in data]
    return ret


route_methods = dict(commands=commands, headlines=headlines, sentiment=sentiment, indicator=indicator, stock=stock, highlow52w=highlow52w)