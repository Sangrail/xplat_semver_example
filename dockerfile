# Use a base image with both Python and CMake
FROM ubuntu:20.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Add version labels
LABEL version="1.0.0"
LABEL description="A mini project with Python, C++, Luigi, and Docker"

# Install dependencies in one RUN statement to use caching effectively
RUN apt-get update && \
    apt-get install -y python3 python3-pip cmake g++ && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy C++ source files and build
COPY cpp/ cpp/
RUN cd cpp && cmake . && make && cp hello_cpp /app/hello_cpp

# Copy Python files
COPY python/ python/
RUN pip3 install -r python/requirements.txt

# Set the entry point
ENTRYPOINT ["python3", "python/luigi_pipeline.py"]