from pathlib import Path
import pandas


def convert_pandas_types(df, folder):
    for col in df:
        if col == "shortName" or col == "sector" or col == "industry" or col == "longBusinessSummary":
            df[col] = df[col].astype(str)
        else:
            df[col] = df[col].astype(float)

    df.to_excel(folder + "/" + k + ".xlsx", index=False)


if __name__ == "__main__":
    database_folder = Path("stockFundamentals") / "database"
    ch = database_folder.resolve().as_posix()
    
    # TODO check if better option available
    stock_fundamentals_csv = ""
    for file in database_folder.glob("*.csv"):
        stock_fundamentals_csv = file

    nseStocks = pandas.read_csv(stock_fundamentals_csv).fillna(0)
    selected_cols = ["shortName", "sector", "industry", "longBusinessSummary", "bookValue", "currentPrice", "currentRatio",
                     "debtToEquity", "earningsGrowth", "ebitda", "ebitdaMargins", "enterpriseToEbitda", "enterpriseToRevenue",
                     "enterpriseValue", "floatShares", "grossMargins", "grossProfits", "heldPercentInsiders",
                     "heldPercentInstitutions",  "operatingCashflow", "operatingMargins",
                     "priceToBook", "profitMargins", "quickRatio", "returnOnAssets", "returnOnEquity", "revenueGrowth",
                     "revenuePerShare", "totalAssets", "totalCash", "totalCashPerShare", "totalDebt", "totalRevenue",
                     "trailingPE"]

    sector_wise_stocks = {}
    for sector in set(nseStocks['sector']):
        if sector != 0:
            sector_wise_stocks[sector] = pandas.DataFrame(columns=selected_cols)

    industry_wise_stocks = {}
    for industry in set(nseStocks['industry']):
        if industry != 0:
            industry_wise_stocks[industry] = pandas.DataFrame(columns=selected_cols)

    for _, entry in nseStocks.iterrows():
        sector = entry['sector']
        industry = entry['industry']
        selected_entry = entry[selected_cols]
        selected_entry_df = pandas.DataFrame(selected_entry).transpose()

        if sector != 0:
            sector_wise_stocks[sector] = sector_wise_stocks[sector].append(selected_entry_df)

        if industry != 0:
            industry_wise_stocks[industry] = industry_wise_stocks[industry].append(selected_entry_df)

    for k, v in sector_wise_stocks.items():
        convert_pandas_types(v, database_folder.resolve().as_posix())

    for k, v in industry_wise_stocks.items():
        convert_pandas_types(v, database_folder.resolve().as_posix())

# Template codes'
# print(nseStocks.shape)
# nseStocks.to_csv("../database/fundamentals/stockFundamentalsWithAnalysis.csv")
# sector_wise_stock = {
#     'Basic Materials': pandas.DataFrame(columns=selected_cols),
#     'Financial Services' : pandas.DataFrame,
#     'Technology'
#     'Industrials',
#     'Financial Services',
#     'Healthcare',
#     'Consumer Cyclical',
#     'Financial Services',
#     'Consumer Defensive',
# 'Energy',
# 'Real Estate'
# 'Communication Services'}
# nseStocks['weights'] = nseStocks["regularMarketPrice"] / nseStocks['revenuePerShare'] + nseStocks['returnOnAssets']
# nseStocks['weights'] = nseStocks['priceToBook']*fundamentals['priceToBook'] + \
#                        nseStocks['priceToSalesTrailing12Months']*fundamentals['priceToSalesTrailing12Months'] +\
#                        nseStocks['returnOnAssets']*fundamentals['returnOnAssets'] + \
#                        nseStocks['returnOnEquity']*fundamentals['returnOnEquity'] + \
#                        nseStocks['revenuePerShare']*fundamentals['revenuePerShare']
