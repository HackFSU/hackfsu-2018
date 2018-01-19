#!/bin/sh

service nginx start
python manage.py runserver 0.0.0.0:8000
