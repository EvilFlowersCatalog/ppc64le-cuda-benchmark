# EvilFlowers OCR Worker

This repository contains a Celery worker that performs OCR (Optical Character Recognition) on PDF files using the
`ocrmypdf` tool. The worker is distributed as a Docker image and is designed to be a part of the EvilFlowers OPDS
catalog ecosystem, providing extended functionality for processing and managing digital content.

## Features

- **OCR Processing:** Automatically processes PDF files to make them searchable using OCR.
- **Distributed Processing:** Uses Celery for distributed task processing, allowing the worker to be scaled as needed.
- **Dockerized:** Packaged as a Docker image for easy deployment and integration with other services in the EvilFlowers
ecosystem.


## Getting Started

### Prerequisites

- Docker installed on your machine.
- A running Redis instance (or any other broker supported by Celery) for task queuing.

### Building the Docker Image

To build the Docker image, use the following command:

```bash
docker build -t evilflowers-ocr-worker .
```

### Running the Docker Container

To run the Docker container, execute the following command:

```bash
docker run -d --name evilflowers-ocr-worker \
    -e BROKER=redis://your_redis_instance:6379/0 \
    evilflowers-ocr-worker
```

## Environment Variables

| Environment Variable          | Description                                                       | Default Value              | Example                       |
|-------------------------------|-------------------------------------------------------------------|----------------------------|-------------------------------|
| `BROKER`                      | The message broker URL for Celery                                 | `redis://localhost:6379/0` | `redis://redis-server:6379/0` |
| `CELERY_WORKER_LOGLEVEL`      | Log level for the Celery worker                                   | `INFO`                     | `DEBUG`                       |
| `CELERY_MAX_RETRIES`          | Maximum number of retries for a failed task                       | `3`                        | `5`                           |
| `CELERY_RETRY_DELAY`          | Delay in seconds before retrying a failed task                    | `60`                       | `120`                         |
| `OTEL_SERVICE_NAME`           | The name of the service for OpenTelemetry tracing                 | `evilflowers-ocr-worker`   | `custom-service-name`         |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | The endpoint of the OpenTelemetry Collector or backend for traces | Not set                    | `http://collector:4317`       |
| `OTEL_LOG_LEVEL`              | Log level for OpenTelemetry-related logs                          | `INFO`                     | `DEBUG`                       |

### Using the OCR Worker from Another Workspace

To call the OCR worker from another workspace using Celery signatures, you need to follow a few steps to ensure proper
configuration and functionality.

Start by ensuring that Celery is properly set up in your workspace and configured to use the same broker (e.g., Redis)
as the OCR worker. This is crucial for enabling communication between your application and the worker.

Next, import the `ocr` task using Celery's `signature` function and pass the necessary arguments. Here is an example:

```python
from celery import signature

# Define the task signature with the necessary arguments
ocr_task = signature("evilflowers_ocr_worker.ocr", args=["/path/to/source.pdf", "/path/to/destination.pdf", "eng"])

# Apply the task asynchronously
result = ocr_task.apply_async()

# Optionally, you can check the result or wait for completion
print(result.get())
```

A critical aspect to consider is filesystem access and mounting. The worker needs access to the files specified in the
input paths (source and destination) to function properly. This can be achieved by ensuring that the file paths are
accessible within the Docker container. The most effective way to achieve this is by using Docker's volume mounting.

For example, when running the worker container, mount the host's directories containing the source and destination
files into the container:

```shell
docker run -d --name evilflowers-ocr-worker \
    -e BROKER=redis://your_redis_instance:6379/0 \
    -v /host/source/directory:/container/source/directory \
    -v /host/destination/directory:/container/destination/directory \
    evilflowers-ocr-worker
```

In this command, `/host/source/directory represents` the path on the host machine where your source PDF files are
located, and `/container/source/directory` is the corresponding path within the Docker container. Similarly,
`/host/destination/directory` is the path on the host machine where the processed PDF files should be saved,
and `/container/destination/directory` is the corresponding path within the Docker container.

By mounting these directories, the worker running inside the Docker container can access the necessary files for
processing.

For more detailed information about Celery signatures and task management, refer to the
[Celery documentation](https://docs.celeryq.dev/en/stable/userguide/calling.html).

## Acknowledgment

This open-source project is maintained by students and PhD candidates of the
[Faculty of Informatics and Information Technologies](https://www.fiit.stuba.sk/) at the Slovak University of
Technology. The software is utilized by the university, aligning with its educational and research activities. We
appreciate the faculty's support of our work and their contribution to the open-source community.

![](docs/images/fiit.png)
