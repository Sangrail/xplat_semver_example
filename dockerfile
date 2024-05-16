# Use a base image with both Python and CMake
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

LABEL version="1.0.0"
LABEL description="A mini project with Python, C++, Luigi, and Docker"

RUN apt-get update && \
    apt-get install -y python3 python3-pip cmake g++ && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY cpp/ cpp/
RUN cd cpp && cmake . && make && cp hello_cpp /app/hello_cpp

COPY python/ python/

COPY .env .

RUN pip3 install -r python/requirements.txt


ENTRYPOINT ["python3", "python/luigi_pipeline.py"]