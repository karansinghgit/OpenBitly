#!/bin/sh
set -e

# Apply migrations against the (possibly empty) volume-backed database before
# the app starts serving traffic.
python manage.py migrate --noinput

exec gunicorn openbitly.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers "${GUNICORN_WORKERS:-3}"
