import time

import pandas
import yfinance as yahooFinance

start = time.time()

nse_stocks = pandas.read_csv("../../database/zerodha/allStockMetaData/allInstrumentNse.csv")
nse_stock_information = pandas.DataFrame()

debug = True
stock_count = 0
try:
    for index, row in nse_stocks.iterrows():
        if debug and stock_count > 5:
            break
        stock_information = yahooFinance.Ticker(row['NseSymbol'] + '.NS')
        column_names = []

        if index == 0:
            column_names = stock_information.info.keys()
            nse_stock_information = pandas.DataFrame(columns=column_names)

        nse_stock_information.loc[index] = stock_information.info
        stock_count += 1

except Exception as e:
    print(e)

print(nse_stock_information.shape)
nse_stock_information.to_csv("../database/fundamentals/stock_information.csv", index=False)
print("Elapsed ", time.time() - start)
