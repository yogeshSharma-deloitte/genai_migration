#!/bin/sh
git config --system core.longpaths true
python manage.py makemigrations
python manage.py migrate
gunicorn -c gunicorn_conf.py ejb_spring_boot.asgi:application &
nginx -g 'daemon off;'