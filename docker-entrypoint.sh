#! /bin/bash

python manage.py collectstatic -v0 --noinput
python manage.py migrate -v0 --noinput
python manage.py loaddata init
#gunicorn project.wsgi -b 0.0.0.0:8000 --timeout 1200
echo " user admin, password: admin "
daphne project.asgi:application -b 0.0.0.0 -p 8000
