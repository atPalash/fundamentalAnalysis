import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
from pathlib import Path
from utility.reader import read_config
import numpy as np
import matplotlib.pyplot as plt
import math
import datetime as dt

def getNseDeliveryData(selectedStocks=True, plot=True):
    headers = {
        'Host': 'www1.nseindia.com',
        'Referer': 'https://www1.nseindia.com/products/content/equities/equities/eq_security.htm',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }

    try:
        database_folder = Path(
            "stockFundamentals/database/delivery").resolve().as_posix()
        conf_folder = Path("conf")
        nse_stocks = pd.read_csv(
            (conf_folder / "ind_NseList.csv").resolve().as_posix())
        selected_nse_stocks = read_config(
            (conf_folder / "selected_stocks.yml").resolve().as_posix())
        selected_stocks = selected_nse_stocks['to_buy'] + \
            selected_nse_stocks['to_sell']
        nse_stock_fundamentals = pd.DataFrame()

        header = []
        rows = []
        count = 0
        stock_plot_data = {}
        # delivery = pd.DataFrame()
        for stock in selected_stocks:
            try:
                api_url = f'https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol={stock}&segmentLink=3&symbolCount=2&series=ALL&dateRange=3month&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE'
                response = requests.get(api_url, headers=headers)
                response = response.content.decode("utf-8")
                # parse the HTML
                soup = BeautifulSoup(response, "html.parser")
                div = soup.find("div", {"id": "csvContentDiv"}).getText()
                data = div.replace(" ", "").split(':')

                if len(header) == 0:
                    header = [data[0].split(',')]
                data.pop(0)

                for l in data:
                    rows.append(l.split(','))
                count += 1
            except Exception as e:
                print(e)
                continue

        dataFrame = pd.DataFrame(data=rows, columns=header)
        dataFrame.to_csv(database_folder + '/delivery.csv',
                         index=False, quoting=csv.QUOTE_NONE)

    except Exception as e:
        print(e)


def plotNseData():
    conf_folder = Path("conf")
    selected_nse_stocks = read_config(
        (conf_folder / "selected_stocks.yml").resolve().as_posix())
    selected_stocks = selected_nse_stocks['to_buy'] + \
    selected_nse_stocks['to_sell']
    dataFrame = pd.read_csv(
            '/home/pi/Dev/fundamentalAnalysis/stockFundamentals/database/delivery/delivery.csv')

    rows = math.ceil((len(selected_stocks) / 3))
    cols = 3

    fig, axs = plt.subplots(rows, cols)
    fig.set_figheight(rows * 3)
    fig.set_figwidth(rows)
    x_count = 0
    y_count = 0
    for stock in selected_stocks:
        try:
            stock_data = dataFrame[dataFrame["Symbol"] == stock]
            # axs[x_count, y_count].scatter(
                    # stock_data['Date'].values, stock_data['DeliverableQty'].values, s=80, marker="*")
            x = stock_data['Date'].values
            y = stock_data['DeliverableQty'].values
            # dates = np.copy(x)
            for i in range(len(y)):
                try:
                    y[i] = int(y[i])
                    # dates[i] = dt.datetime.strptime(dates[i], "%d-%b-%Y")
                except Exception as e:
                    y[i] = y[i-1]
                    # print(e)
                
            axs[x_count, y_count].scatter(x, y, s=80, marker="o")
            # axs[x_count, y_count].set_xticklabels([date.month for date in dates])
            axs[x_count, y_count].set_xticks([])
            axs[x_count, y_count].set_title(stock)
            
            y_count += 1
            if y_count == cols:
                x_count += 1
                y_count = 0
        except Exception as e:
            print(e)
            continue

    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    # plt.show()
    plt.savefig('foo.png')

if __name__ == "__main__":
    getNseDeliveryData()
    plotNseData()
    # ti = "07-Dec-2022"
    # td = dt.datetime.strptime(ti, "%d-%b-%Y").date()
    # print(td)

#######
# api_url = 'https://www1.nseindia.com/products/dynaContent/common/productsSymbolMapping.jsp?symbol=ABB&segmentLink=3&symbolCount=2&series=ALL&dateRange=3month&fromDate=&toDate=&dataType=PRICEVOLUMEDELIVERABLE'

# headers = {
# 'Accept': '*/*',
# 'Accept-Encoding': 'gzip, deflate, br',
# 'Accept-Language': 'en-GB,en;q=0.6',
# 'Connection': 'keep-alive',
# 'Cookie': 'pointer_il=1; sym_il1=CREATIVEYE; NSE-TEST-1=1944068106.20480.0000; ak_bmsc=8761366CB501203B697A2C441EB79DCE~000000000000000000000000000000~YAAQRf1zPvwPA5yEAQAAKbnn5xLYn7xmoqpwp1hUWg0NTy+oZVXBYOpIVIZpvrGxWEkshKBaNJGR8F0T4Pt4i2ndDLOcQDC0UF7ylQl6EVDfj6thy4g1U7E7EIN6YFtZEAlynB8jDuPFmYwg+pwupGYbMywYCzwpG/xRTBTIauTh8/7RnAwH/UeXtjaH8qVw/t3QQ7dByQ0cITmcS78ea/KAFtRwy7yrbOZXIUAA+A4YxqfiRa5awRWSkrNLJvkbOnIt+O2iIyNY0Vvb0IHnl27HehoJbtaWZJz5RU6Ey/l82WGOKo+2khwpJWoE2UwCxo/MM1U3rZVMlp+XrGzjDXq/TT8sBVbjFleJEKkTQjH7Ng34AjveiGZAF82trLUqDA==; JSESSIONID=FA121BB516C4EEF87BF9D264B03F53A1.tomcat2; bm_mi=111E11EA8B9C28BD8D8FF437CED2B65E~YAAQRf1zPjJAA5yEAQAAOXzz5xI2WevxtqGtI+XxfPpaZu7x6kSRz0ThnqWO/xNZ9uyQKyW+Kcj5oNxNzKEZL1nQQWGdc3jmeNVCKj6XSaxjBJtAFcf00KaQkFJtdVwtLnYN9PvytEHtvyPWoMtoG59U+SrW7Pahci4iB5w+AFJNr/vGM1vvj8epOHiW5I6tIAIK6EAZ+vrFXxpcEQfBXs+EMZcbojZjJjLeLl6ExfH81pY3VQ+Q0KdxI1IvGO75j6cgPzb/JrhNbXMjh69fRd3pMaT3cCFDqodzicB8fHgJeL2EMs/dPkwINeA/ZhqGOsE1bqRTX2KbOcErcZVchDXiG1Cuz/ZZTY9YEPIEjw==~1; bm_sv=5CAEFB964596A3EC221EBB8DF8089ABF~YAAQRf1zPjNAA5yEAQAAOXzz5xL6W/ZKonc+N/y2/4lyiel7ATWP+EOSGw6EN3UcXbPvFmdOxKuJZd50TZ0iwDZGLLTykRagKNLDqrflBsIpxI0fG5vJlqiHzudC6GZAGuu0Wkos2oTxFY41warcOHaupwz8/OHfNckTO5DkZv+HNvYfeqvcPQIbTlNDjY/bGn9z6uArmPnk8Oia4YYqwDExfr6/v8c4F14m/ixZ5q1lHZHpgmm7POS/EyAC7ltXGf8=~1',
# 'Host': 'www1.nseindia.com',
# 'Referer': 'https://www1.nseindia.com/products/content/equities/equities/eq_security.htm',
# 'Sec-Fetch-Dest': 'empty',
# 'Sec-Fetch-Mode': 'cors',
# 'Sec-Fetch-Site': 'same-origin',
# 'Sec-GPC': '1',
# 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
# 'X-Requested-With': 'XMLHttpRequest',
# 'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Brave";v="108"',
# 'sec-ch-ua-mobile': '?0',
# 'sec-ch-ua-platform': '"Windows"'
# }
