#!/bin/sh
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput
[ ! -d "./media" ] && python manage.py populate_db
exec "$@"
