#!/bin/sh

if [ ! -d "./local-env" ]; then
  python -m venv ./local-env && \
  chmod 755 local-env/bin/activate
fi

# Activate the virtual environment and setup tools
source ./local-env/bin/activate
python3 -m pip install -U pip setuptools poetry watchdog
poetry install --no-root

# Run the web server
watchmedo auto-restart --patterns="*.py" --recursive -- python -B main.py
