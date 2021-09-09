FROM alpine:3.14

RUN apk update
RUN apk add ruby

# RUN gem install bundler
RUN gem install rspec=3.7.2