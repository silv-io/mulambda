FROM python:3.11

WORKDIR /code
COPY Makefile /code/Makefile

# copy requirements
COPY requirements.txt /code/requirements.txt
# make venv
RUN make venv
# pip install requirements
RUN make install-requirements

COPY . /code

RUN make install-docker

ENTRYPOINT ["make", "run"]
