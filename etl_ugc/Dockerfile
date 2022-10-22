FROM python:3.10-slim


WORKDIR /etl_ugc/

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir\
    && pip install -r requirements.txt --no-cache-dir

COPY . /etl_ugc/

RUN apt update && apt install -y netcat && chmod +x entrypoin.sh

ENTRYPOINT ./entrypoin.sh && python ./src/main.py
