FROM --platform=linux/amd64 python:3.12
LABEL authors="mugdhakolte"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# install dependencies
RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y libpq-dev

COPY requirements.txt /code/

RUN pip install -r requirements.txt
COPY . /code/
COPY .env /code/.env