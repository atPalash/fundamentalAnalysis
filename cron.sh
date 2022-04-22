#!/bin/sh
cd "$(dirname "$0")";
CWD="$(pwd)"

# copy previous logs
cp $CWD/logs/*.log $CWD/logs/previous/
# remove previous log
rm -rf $CWD/logs/*.log
# start analysis loop
$CWD/.venv/bin/python $CWD/main.py