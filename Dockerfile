FROM --platform=linux/amd64 python:3.12.3-slim
LABEL authors="mugdhakolte"

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y libpq-dev && apt-get clean

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
COPY ./requirements-dev.txt /usr/src/app/requirements-dev.txt
RUN pip install -r requirements-dev.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# add app
COPY . .

RUN chmod +x /usr/src/app/entrypoint.sh
# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]