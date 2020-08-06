#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
exec "$@"
