#!/bin/sh
cd "$(dirname "$0")";
CWD="$(pwd)"
echo $CWD
$CWD/.venv/bin/python $CWD/main.py