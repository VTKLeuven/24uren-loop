FROM python:3.8-alpine

RUN apk update && apk add gcc

ENV HOME /home/src/locust
RUN mkdir -p $HOME
WORKDIR $HOME

ENV PYTHONUNBUFFERED 1

COPY requirements.txt $HOME
RUN pip install -r $HOME/requirements.txt

COPY . $HOME


