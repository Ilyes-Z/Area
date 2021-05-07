FROM python:3.8

RUN mkdir -p /usr/src/api

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/api

COPY requirements.txt /usr/src/api

RUN pip install -r requirements.txt