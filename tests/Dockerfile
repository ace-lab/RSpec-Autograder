FROM alpine:3.14

RUN mkdir /grade
RUN mkdir /grade/data
RUN mkdir /grade/results
RUN mkdir /grade/serverFilesCourse
RUN mkdir /grade/serverFilesCourse/suites
RUN mkdir /grade/student
RUN mkdir /grade/tests
RUN mkdir /grade/grader

COPY .testing/data/ /grade/data
COPY .testing/results/ /grade/results
COPY .testing/serverFilesCourse/ /grade/serverFilesCourse
COPY .testing/student/ /grade/student
COPY .testing/tests /grade/tests
COPY .testing/grader/ /grade/grader

RUN apk update
RUN apk add --no-cache python3
RUN ls /grade | less
RUN chmod +x /grade/grader/run.py

RUN apk add --no-cache ruby

# RUN adduser -D autograder
# USER autograder
RUN echo 'gem: --no-document' > /etc/gemrc && \
    gem install bundler
RUN gem update --system
RUN /grade/grader/run.py

RUN diff expected created