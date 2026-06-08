# syntax=docker/dockerfile:1
FROM python:3
RUN useradd -ms /bin/sh -u 1001 app
USER app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code/backend
COPY requirements.txt /code/backend/
RUN pip install -r requirements.txt
COPY --chown=app:app . /code/backend/