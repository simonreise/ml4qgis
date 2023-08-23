# FROM python:3.10-slim as builder
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04 as original
# FROM tensorflow/tensorflow:latest-gpu as builder

ARG PYTHON_VERSION=3.10

RUN sed -i 's/archive.ubuntu.com/en.archive.ubuntu.com/g' /etc/apt/sources.list &&\
	apt-get --allow-releaseinfo-change update &&\
	apt-get install -y --no-install-recommends --no-install-suggests \
	python${PYTHON_VERSION} \
	python3-pip \
	python${PYTHON_VERSION}-dev \
	python${PYTHON_VERSION}-venv \
	file \
    && cd /usr/bin \
    && ln -sf python${PYTHON_VERSION}         python3 \
    && ln -sf python${PYTHON_VERSION}m        python3m \
    && ln -sf python${PYTHON_VERSION}-config  python3-config \
    && ln -sf python${PYTHON_VERSION}m-config python3m-config \
    && ln -sf python3                         /usr/bin/python \
    && python -m pip install --upgrade pip \
    && python -m pip install --upgrade \
        setuptools


FROM original as builder

WORKDIR /app

ENV HOME /app

COPY requirements.txt .

RUN python3 -m venv /app/venv

RUN . /app/venv/bin/activate && python3 -m pip install -r requirements.txt --default-timeout=1000

ADD https://step.esa.int/thirdparties/sen2cor/2.11.0/Sen2Cor-02.11.00-Linux64.run .

RUN chmod +x Sen2Cor-02.11.00-Linux64.run && ./Sen2Cor-02.11.00-Linux64.run --target /app/.snap/auxdata/Sen2Cor-02.11.00-Linux64



# FROM python:3.10-slim
# FROM tensorflow/tensorflow:latest-gpu
FROM original

WORKDIR /app

ENV HOME /app

COPY --from=builder /app/venv /app/venv

COPY --from=builder /app/.snap/auxdata/Sen2Cor-02.11.00-Linux64/ /app/.snap/auxdata/Sen2Cor-02.11.00-Linux64/

COPY --from=builder /app/sen2cor/ /app/sen2cor/

RUN echo '/app/.snap/auxdata/Sen2Cor-02.11.00-Linux64/lib' >> /etc/ld.so.conf \
	&& ldconfig
