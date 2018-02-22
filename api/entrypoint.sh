#!/bin/sh

python manage.py collectstatic --noinput
service nginx start
service nginx status
python manage.py runserver 0.0.0.0:8000
