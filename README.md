# Fundamental analysis checker
Work in progress

# Cron command
```cron I'm A tab
15 9 * * *  /home/pi/Dev/fundamentalAnalysis/cron.sh >> /home/pi/Dev/fundamentalAnalysis/cronlog.txt 2>&1
```
# Stock selector
ROA + PE in top bracket for stock having considerable Capital.

# TODO
1. Fetch fundamentals like market, ROA, margin etc. each month and select top stocks.
2. Select accurate entry points using RSI.
3. Implement/test other indicators.
4. Check indicator value for each stock using stock name.
5. Keep track of all the stocks bought maybe possible from zerodha app. Download the file and keep it here.
3. 

 1639  python3 -m pip install tensorflow --no-cache-dir
 1640  pip list
 1641  python3 -m pip install sklearn pandas --no-cache-dir
 1642  python3 -m pip install matplotlib --no-cache-dir
 1643  python3 -m pip install yahoo-fin plotly --no-cache-dir
 1644  python3 -m pip install discord --no-cache-dir
 1645  python3 -m pip install pyyaml --no-cache-dir
 1646  python3 -m pip install yfinance --no-cache-dir

  1639  python3 -m pip install tensorflow sklearn pandas matplotlib yahoo-fin discord pyyaml yfinance --no-cache-dir
 
 1641  python3 -m pip install sklearn pandas --no-cache-dir
 1642  python3 -m pip install matplotlib --no-cache-dir
 1643  python3 -m pip install yahoo-fin plotly --no-cache-dir
 1644  python3 -m pip install discord --no-cache-dir
 1645  python3 -m pip install pyyaml --no-cache-dir
 1646  python3 -m pip install yfinance --no-cache-dir