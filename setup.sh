#!/usr/bin/env bash

# setup linter check before commit
flake8 --install-hook git
git config --bool flake8.strict true

# setup dpendency
pip install -r ./requirements/dev.txt

python manage.py makemigrations

python manage.py migrate
coverage run --source="./apps" manage.py test -v0
coverage report

python manage.py collectstatic -v0 --noinput
echo -n "Создать суперпользователя? (y/N)"

read -r item
case "$item" in
y | Y)
  python manage.py createsuperuser
  ;;
n | N)
  exit
  ;;
*) ;;

esac

python manage.py runserver
