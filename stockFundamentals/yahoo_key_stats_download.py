from datetime import datetime
from pathlib import Path
import time

import pandas
import yfinance as yahooFinance

start = time.time()
try:
    database_folder = Path("stockFundamentals/database")
    conf_folder = Path("conf")
    nse_stocks = pandas.read_csv((conf_folder / "ind_NseList.csv").resolve().as_posix())
    nse_stock_fundamentals = pandas.DataFrame()

    debug = True
    stock_count = 0
    try:
        for index, row in nse_stocks.iterrows():
            if debug and stock_count > 2:
                break
            stock_fundamentals = yahooFinance.Ticker(row['NseSymbol'] + '.NS')
            column_names = []

            if index == 0:
                column_names = stock_fundamentals.info.keys()
                nse_stock_fundamentals = pandas.DataFrame(columns=column_names)

            nse_stock_fundamentals.loc[index] = stock_fundamentals.info
            stock_count += 1

    except Exception as e:
        print(e)

    print(nse_stock_fundamentals.shape)
    date_time = datetime.now().strftime('%H_%M_%d_%m_%Y')
    nse_stock_fundamentals.to_csv((database_folder / f"{date_time}_stock_fundamentals.csv").resolve().as_posix(), index=False)
    print("Elapsed ", time.time() - start)
except Exception as e:
    print(e)