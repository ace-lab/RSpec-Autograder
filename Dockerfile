FROM alpine:3.14

RUN mkdir /grader
WORKDIR /grade
COPY grader /grader
RUN apk update

RUN apk add --no-cache python3
RUN chmod +x /grader/run.py
# maybe install py3-pip

RUN apk add --no-cache ruby
RUN gem install bundler
# RUN gem install rspec

