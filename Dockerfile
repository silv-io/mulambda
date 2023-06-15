FROM python:3.11

WORKDIR /code

COPY . /code

RUN make install-docker

ENTRYPOINT ["make", "run"]
