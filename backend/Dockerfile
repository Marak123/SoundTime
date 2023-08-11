FROM python:3.11-alpine3.18

ENV PYTHONUNBUFFERED 1

WORKDIR /django
COPY ./requirements.txt /requirements.txt

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install -r /requirements.txt

COPY . .