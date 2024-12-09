# Stage 1: Base CUDA image
FROM nvidia/cuda:12.2.2-base-ubuntu22.04 AS base


RUN apt-get -y update \
    && apt-get install -y software-properties-common \
    && apt-get -y update \
    && add-apt-repository universe
RUN apt-get -y update
RUN apt-get -y install python3.11 python3-pip

WORKDIR /issai_qazllm

COPY requirements.txt .

RUN pip install -r requirements.txt

