FROM alpine:3.14

ENV BUILD_PACKAGES ruby-dev
RUN apk add bash $BUILD_PACKAGES

RUN mkdir /grade
RUN mkdir /grade/data
RUN mkdir /grade/results
RUN mkdir /grade/serverFilesCourse
RUN mkdir /grade/serverFilesCourse/suites
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
# RUN ls /grade | less
RUN chmod 777 /grade 

RUN apk add --no-cache ruby ruby-bundler build-base

RUN gem install json
# RUN gem install diff-lcs -v '1.4.4' --source 'https://rubygems.org/'
# RUN gem install rspec-support -v '3.10.2' --source 'https://rubygems.org/'

# RUN adduser -D autograder
# RUN chown autograder /grade
# USER autograder
# RUN /grade/grader/run.py
# RUN ls /grade/working

# RUN diff expected created