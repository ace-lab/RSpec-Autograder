FROM alpine:3.14

RUN apk add bash ruby-dev

RUN mkdir /grade
RUN mkdir /grade/data
RUN mkdir /grade/results
RUN mkdir /grade/serverFilesCourse
RUN mkdir /grade/student
RUN mkdir /grade/tests
RUN mkdir /grader

COPY .testing/data/ /grade/data
COPY .testing/results/ /grade/results
COPY .testing/serverFilesCourse/ /grade/serverFilesCourse
COPY .testing/student/ /grade/student
COPY .testing/tests /grade/tests
COPY .testing/grader/ /grader

RUN apk update 
RUN apk upgrade
RUN apk add --no-cache python3
# RUN chmod 777 /grade 

RUN apk add --no-cache ruby ruby-bundler build-base

RUN gem install json