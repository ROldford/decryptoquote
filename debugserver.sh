#!/bin/sh

export FLASK_APP=./app.py
export FLASK_ENV=development
."$(pipenv --venv)"/bin/activate
flask run -h 0.0.0.0
