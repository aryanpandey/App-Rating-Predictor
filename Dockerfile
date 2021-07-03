FROM ubuntu:20.04

ENV DEBIAN_FRONTEND noninteractive

LABEL maintainer="Aryan Pandey <aryan.pandey@outlook.com>"

RUN apt-get update --fix-missing && apt-get install -y wget bzip2 ca-certificates \
      build-essential \
      curl \
      git-core \
      htop \
      pkg-config \
      python3-dev \
      python3-pip \
      python-setuptools \
      unzip \
      && \
      apt-get clean

COPY requirements.txt /tmp
WORKDIR /tmp

RUN pip3 install -r requirements.txt

