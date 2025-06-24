#!/bin/sh

if [ ! -d "./local-env" ]; then
  python -m venv ./local-env && \
  chmod 755 local-env/bin/activate
fi

# Activate the virtual environment and setup tools
source ./local-env/bin/activate
python3 -m pip install -U pip setuptools poetry
poetry install --no-root

# python -B main.py
