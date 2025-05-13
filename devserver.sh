#!/bin/sh
source .venv/bin/activate
python src/manage.py runserver $PORT
