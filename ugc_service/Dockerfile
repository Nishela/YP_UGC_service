FROM python:3.10-slim

WORKDIR /ugc_service

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt .

RUN pip install --upgrade pip --no-cache-dir\
    && pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

COPY ./src .
COPY entrypoin.sh .

RUN apt update && apt install -y netcat && chmod +x entrypoin.sh

ENTRYPOINT ./entrypoin.sh && python main.py
