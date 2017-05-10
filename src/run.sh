#!/usr/bin/env bash
LANGUAGE_CODE='de-de'
export LANGUAGE_CODE
P='django_project/django_project'
sed -e 's:{{getv "/elefant/language-code"}}:"'$LANGUAGE_CODE'":' \
    -e 's:{{getv "/elefant/time-zone"}}:"Europe/Berlin":' "${P}/settings.py.tmpl" >"${P}/settings.py"