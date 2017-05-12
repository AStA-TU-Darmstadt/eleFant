#!/usr/bin/env bash

cd django_project
python manage.py collectstatic # collect static files in a single directory
python manage.py makemigrations elefant
python manage.py migrate # make django migrations
service nginx start # start nginx
uwsgi --uid=1000 --gid=2000 --ini /code/uwsgi.ini # start uwsgi server with user privileges