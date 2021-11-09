FROM alpine:3.14

RUN apk update 
RUN apk upgrade
RUN apk add bash ruby-dev
RUN apk add --no-cache python3

RUN apk add --no-cache ruby ruby-bundler build-base

RUN gem install json rspec

RUN mkdir /grader
COPY grader /grader
RUN chmod +x /grader/run.py