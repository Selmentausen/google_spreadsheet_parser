#!/bin/sh

if [ "$1" = cron ]; then
  ./manage.py crontab add
else
  python manage.py flush --no-input
  python manage.py migrate
  python manage.py crontab add
  python manage.py crontab show
fi

if [ "$DATABASE" = "postgres" ]; then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

exec "$@"