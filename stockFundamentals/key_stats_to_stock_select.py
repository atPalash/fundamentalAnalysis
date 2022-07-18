from datetime import datetime
import os
from pathlib import Path
import pandas
import shutil
import yahoo_key_stats_download

def check_folder_path(folder_path:str):
    """
    checks for existence of folder at path. if not present creates one.
    Args:
        folder_path (str): folder path to check or create.
    """
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

def convert_pandas_types(df, folder):
    for col in df:
        if col == "shortName" or col == "sector" or col == "industry" or col == "longBusinessSummary":
            df[col] = df[col].astype(str)
        else:
            df[col] = df[col].astype(float)
            
    check_folder_path(folder)
    df.to_excel(folder + "/" + k + ".xlsx", index=False)


if __name__ == "__main__":
    date_time = datetime.now().strftime('%Y_%m_%d_%H_%M')
    current_working_directory = Path("stockFundamentals")
    database_folder = current_working_directory / "database"
    previous_database_folder = database_folder / "previous"
    
    database_folder_path = database_folder.resolve(strict=True).as_posix()
    previous_database_path = previous_database_folder.resolve(strict=True).as_posix()
    
    # move previous fundamentals
    for file in os.listdir(database_folder_path):
        if not file.endswith('previous'):
            shutil.move(os.path.join(database_folder_path, file), os.path.join(previous_database_path, file))
         
    # Download latest fundamentals, this creates a csv file of fundamental data of all Nse stocks.
    latest_fundamentals_folder = os.path.join(database_folder_path, date_time)
    csv_name = "stock_fundamentals.csv"
    os.makedirs(latest_fundamentals_folder)
    stock_fundamentals_csv_path = os.path.join(latest_fundamentals_folder, csv_name) 
    yahoo_key_stats_download.download_latest_fundamentals(stock_csv_path=stock_fundamentals_csv_path, debug=False)

    nseStocks = pandas.read_csv(stock_fundamentals_csv_path).fillna(0)
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
        selected_entry_df["ROA + PE"] = selected_entry_df["trailingPE"] + selected_entry_df["returnOnAssets"]
        if sector != 0:
            sector_wise_stocks[sector] = sector_wise_stocks[sector].append(selected_entry_df)

        if industry != 0:
            industry_wise_stocks[industry] = industry_wise_stocks[industry].append(selected_entry_df)

    for k, v in sector_wise_stocks.items():
        convert_pandas_types(v, f"{latest_fundamentals_folder}/sector")

    for k, v in industry_wise_stocks.items():
        convert_pandas_types(v, f"{latest_fundamentals_folder}/industry")

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
