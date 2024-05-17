# Mini Project: Python, C++, Luigi, Docker, and GitHub Actions

## Overview

This project demonstrates how to integrate Python, C++, Luigi, Docker, and GitHub Actions. It includes:
- A simple C++ program that prints "Hello from C++!"
- A Python script that runs the C++ program
- A Luigi pipeline to orchestrate the workflow
- Docker for containerization
- GitHub Actions for CI/CD

## Project Structure

```
root/
├── cpp/
│   ├── CMakeLists.txt
│   └── main.cpp
├── python/
│   ├── main.py
│   ├── luigi_pipeline.py
│   └── requirements.txt
├── Dockerfile
├── README.md
└── .gitignore
```
## Getting Started

### Prerequisites

- Docker
- Git

### Building and Running the Docker Container

1. Clone the repository:

2. Build the Docker image:

    ```sh
    docker build -t myproject:latest .
    ```

3. Run the Docker container:

    ```sh
    docker run myproject:latest
    ```


Sample telemetry for the entire Luigi Pipeline, including the luigi nodes and c++ subprocess:

![](/imgs/telemetry.png)