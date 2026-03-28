#!/bin/sh

python manage.py migrate --noinput

mkdir -p /backend/staticfiles /backend/media
python manage.py collectstatic --noinput

python admin.py

exec "$@"
