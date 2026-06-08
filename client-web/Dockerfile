# syntax=docker/dockerfile:1
FROM node:18-alpine
RUN useradd -ms /bin/sh -u 1001 app
USER app
WORKDIR /code/client-web
COPY package.json /code/client-web
RUN apk add --update git
RUN npm install
COPY --chown=app:app . /code/client-web/