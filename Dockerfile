FROM alpine:3.14

RUN apt update
RUN apk add ruby

RUN gem install bundler
RUN gem install rspec