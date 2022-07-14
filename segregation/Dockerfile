FROM python:3.9.6-slim

RUN apt-get update

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app

RUN pip install --upgrade pip \
    pip install -r requirements.txt