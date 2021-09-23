FROM alpine:3.14

RUN apk update

RUN apk add --no-cache python3
RUN chmod +x setup.py
# maybe install py3-pip

ENV GRADING_SCRIPT "ruby"
RUN apk add --no-cache ruby
# RUN gem install bundler
RUN gem install rspec=3.7.2

