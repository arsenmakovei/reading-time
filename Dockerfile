FROM python:3.10-slim-buster
LABEL maintainer="makoveyarsen@gmail.com"

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
