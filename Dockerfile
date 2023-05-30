FROM python:3.10 as python-base

WORKDIR  /code

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY . .
RUN poetry install

