#!/bin/sh
cd "$(dirname "$1")" || exit
CWD="$(pwd)"

echo $CWD downloading fundamentals and converting to excel
$CWD/.venv/bin/python $CWD/stockFundamentals/key_stats_to_stock_select.py