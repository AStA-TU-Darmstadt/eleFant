#!/usr/bin/env bash

# parameters for django settings
LANGUAGE_CODE='de-de'
export LANGUAGE_CODE
python manage.py migrate
python manage.py runserver