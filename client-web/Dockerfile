# syntax=docker/dockerfile:1s
FROM node:18
RUN useradd -ms /bin/sh -u 1001 app
USER app
WORKDIR /code/client-web
COPY package.json /code/client-web
RUN npm install
COPY --chown=app:app . /code/client-web/