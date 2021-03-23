FROM continuumio/miniconda3 AS build

# https://pythonspeed.com/articles/conda-docker-image-size/

# Install conda-pack:
RUN conda install -c conda-forge conda-pack

# Install the package as normal:
COPY conda-env.yml .
RUN conda env create -f conda-env.yml 

RUN mkdir -p /opt/chem_kit/
WORKDIR /opt/chem_kit
COPY pyproject.toml  /opt/chem_kit/pyproject.toml
COPY poetry.lock  /opt/chem_kit/poetry.lock

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN . $HOME/.poetry/env && conda run -n chem_kit_api poetry install --no-dev

# Use conda-pack to create a standalone enviornment
# in /venv:
RUN conda-pack -n chem_kit_api -o /tmp/env.tar && \
  mkdir /venv && cd /venv && tar xf /tmp/env.tar && \
  rm /tmp/env.tar

# We've put venv in same path it'll be in final image,
# so now fix up paths:
RUN /venv/bin/conda-unpack
RUN rm -R /venv/share
RUN rm -R /venv/conda-meta
RUN rm -R /venv/include/
RUN rm -R /venv/lib/sqlite3.30.1.2/
RUN rm -R /venv/lib/tk8.6/

# The runtime-stage image; we can use Debian as the
# base image since the Conda env also includes Python
# for us.
FROM debian:buster-slim

RUN mkdir -p /opt/chem_kit/ && adduser --no-create-home --disabled-password --system web 
COPY --from=build --chown=web:nogroup /venv /venv 
RUN chmod u+x /venv/bin/activate

COPY ./chem_kit_api /opt/chem_kit_api
WORKDIR /opt/chem_kit_api

SHELL ["/bin/bash", "-c"]
CMD source /venv/bin/activate && gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT main:app 
