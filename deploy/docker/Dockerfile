FROM python:3.8-alpine

RUN mkdir /app
WORKDIR /app
ADD ./src/requirements.txt .

RUN apk add --no-cache \
    build-base \
    && adduser --disabled-password --gecos '' app \
    && python3 -m venv /venv \
    && /venv/bin/pip install --no-cache-dir -r /app/requirements.txt

ADD ./src .