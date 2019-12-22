#!/usr/bin/env bash

# setup linter check before commit
if [ -e .flake8 ]; then
  echo "skeep flake8 install."
else
  flake8 --install-hook git
  git config --bool flake8.strict true
fi

# clear old packages (may be wrong installed)
echo -n "clear installed packages? (y/N)"
read -r item
case "$item" in
y | Y)
  pip freeze | xargs pip uninstall -y
  ;;
n | N)
  exit
  ;;
*) ;;
esac

# setup dpendency
pip install -r ./requirements.txt

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

#python manage.py runserver
daphne project.asgi:application
