# pull official base image
FROM python:3.7

RUN mkdir /app
WORKDIR /app
RUN mkdir /static

# install psycopg2 dependencies
RUN apt-get -y update
RUN apt-get install -y gcc python3-dev musl-dev
RUN apt-get install -y gettext

RUN pip install --upgrade pip
RUN mkdir /app/requirements
COPY ./requirements/production.txt ./requirements/production.txt
RUN pip install -r requirements/production.txt
CMD gunicorn -b 0.0.0.0:80 --workers 3 config.wsgi:application
