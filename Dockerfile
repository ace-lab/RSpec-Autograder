FROM alpine:3.14

RUN mkdir /grader
COPY grader /grader

RUN apk update 
RUN apk upgrade
RUN apk add bash ruby-dev
RUN apk add --no-cache python3

RUN apk add --no-cache ruby ruby-bundler build-base

RUN gem install json