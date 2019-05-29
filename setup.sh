#!/usr/bin/env bash

pip install -r ./requirements.txt

python manage.py makemigrations
python manage.py migrate
pytest

python manage.py createsuperuser
python manage.py runserver
