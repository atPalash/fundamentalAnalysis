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