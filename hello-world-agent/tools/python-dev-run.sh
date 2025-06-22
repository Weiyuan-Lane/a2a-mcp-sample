#!/bin/sh

if [ ! -d "./local-env" ]; then
  python -m venv ./local-env && \
  chmod 755 local-env/bin/activate
fi

source ./local-env/bin/activate

pip install -r requirements.txt
python -B main.py
