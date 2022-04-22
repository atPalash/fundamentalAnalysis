#!/bin/sh
cd "$(dirname "$1")";
CWD="$(pwd)"

# copy previous logs
cp $CWD/stockFundamentals/database/*.csv $CWD/stockFundamentals/database/previous/
cp $CWD/stockFundamentals/database/*.xlsx $CWD/stockFundamentals/database/previous/
# remove previous log
rm -rf $CWD/stockFundamentals/database/*.csv
rm -rf $CWD/stockFundamentals/database/*.xlsx

echo $CWD downloading fundamentals from yahoo
# $CWD/.venv/bin/python $CWD/stockFundamentals/yahoo_key_stats_download.py

echo $CWD parsing csv as excel
$CWD/.venv/bin/python $CWD/stockFundamentals/key_stats_to_stock_select.py