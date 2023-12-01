# pull official base image
FROM python:3.10.13-bookworm

# set work directory
WORKDIR /usr/src/django_food_truck

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get upgrade -y
RUN apt install -y netcat-traditional

# install psycopg2 dependencies
RUN apt-get install -y libpq-dev python3-dev

# Install system dependencies for GeoDjango - https://docs.djangoproject.com/en/4.2/ref/contrib/gis/install/geolibs/
RUN apt-get install -y binutils libproj-dev gdal-bin

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/django_food_truck/entrypoint.sh
RUN chmod +x /usr/src/django_food_truck/entrypoint.sh

# copy project
COPY .. .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/django_food_truck/entrypoint.sh"]

RUN unset DJANGO_SUPERUSER_USERNAME && unset DJANGO_SUPERUSER_EMAIL && unset DJANGO_SUPERUSER_PASSWORD