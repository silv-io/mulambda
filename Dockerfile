FROM python:3.11

WORKDIR /code

# copy requirements
COPY requirements.txt /code/requirements.txt
# make venv and install requ
RUN python -m venv .venv && \
    . .venv/bin/activate &&  \
    pip install --upgrade pip setuptools && \
    pip install -r requirements.txt

# pip install requirements

COPY . /code

RUN make install-docker

ENTRYPOINT ["make", "run"]
