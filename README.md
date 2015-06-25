# rabbitmq_exporter_cloudwatch

Simple exporter for rabbitmq data.

## Functionality

It exports length of the selected rabbitmq queues to AWS cloudwatch. It can be useful for AWS autoscaling.


## Configuration

Exporter is configurable via `config.json` file. `example_config.json` shows how it should be configured.

## Installation

- first create your own config.json file,
- then install requirements:

```{bash}
$ pip install -r requirements.txt
```

- make sure that you have exported environment variables authorizing you to
AWS (boto requirement).

## Usage

```{bash}
$ ./main.py
```

Exporter will start exporting data to cloudwatch every 30 seconds.