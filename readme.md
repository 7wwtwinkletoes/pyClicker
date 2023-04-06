### PyClicker
This app automates fishing in Ragnarok Online X (ROX). It works by looking at the fishing button circle and detects the green glow which triggers the mouse click. 

This app can also be modified to automate other similar tasks.

#### Prerequisites:
  - python 3
  - venv

#### Steps to run:
create local python virtual environment

`python -m venv venv`

load the environment

`source ./venv/bin/activate`

make sure build tools are installed

`pip install --upgrade pip setuptools wheel`

install libraries

`pip install -r requirements.txt`

run the app

`python ./app.py`
