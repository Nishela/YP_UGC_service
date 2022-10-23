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

CMD python main.py
