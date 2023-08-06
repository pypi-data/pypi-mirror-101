#!/usr/bin/env sh


python3 manage.py makemigrations $*
#python manage.py migrate --fake-initial $*
python3 manage.py migrate $*
