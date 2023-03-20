#!/bin/sh
# TEFT-MSOFFICE
# version 0.3

python3 -m venv ./venv
source ./venv/bin/activate

./venv/bin/pip install -r requirements.txt
