FROM python:3.7
ENV PYTHONUNBUFFERED 1

RUN apt-get update -y
RUN apt-get install -y gettext

RUN mkdir /app
WORKDIR /app
RUN mkdir /app/requirements
COPY ./requirements ./requirements

RUN pip install -r requirements/local.txt
COPY . /app/
CMD python3.7 manage.py runserver 0.0.0.0:8000