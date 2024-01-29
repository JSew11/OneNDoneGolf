# syntax=docker/dockerfile:1
FROM node:18-alpine
WORKDIR /code/client-web
COPY package.json /code/client-web
RUN apk add --update git
RUN npm install
COPY . /code/client-web/