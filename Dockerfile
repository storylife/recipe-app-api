FROM python:3.7-alpine
MAINTAINER Goodsquirrel Apps

# because of issues when running python from a Docker image
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client

# temporarily install dependencies needed only to install postgresql
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev

RUN pip install -r /requirements.txt

# delete temp dependencies only needed to install postgres
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# For security:
RUN adduser -D user
USER user
