#!/usr/bin/env bash

# parameters for django settings
cd django_project
python manage.py migrate
python manage.py runserver 0.0.0.0:8000