#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# echo "Waiting for service..."

# while ! nc -z service_name 4444; do
#   sleep 0.1
# done

# echo "Service started"


python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate --noinput

# ADD DATA - fixtures
# python manage.py loaddata food-truck-data.csv

# RUN TESTS EVERYTIME
# python manage.py test django_food_truck.finder &> test.log

# CREATE SUPER USER
echo "Creating Super User..."
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL

history -c

exec "$@"