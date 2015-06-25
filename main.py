#!/usr/bin/env python
import json
import time

import boto.ec2.cloudwatch
import requests
from requests.auth import HTTPBasicAuth

TIME_BETWEEN_CHECKS = 30


class Exporter(object):
    def __init__(self):
        with open('config.json', 'r') as f:
            config = json.loads(f.read())

        region = config.get('region', 'eu-west-1')
        self.cloudwatch = boto.ec2.cloudwatch.connect_to_region(region)

        self.metric_namespace = config.get('metric_namespace', 'My/Metric')
        self.queue_to_metric_name = config.get('queue_to_metric_name', {})
        self.interesting_queues = self.queue_to_metric_name.keys()

        self.url = config.get('url', '')
        user = config.get('user', '')
        password = config.get('password', '')
        self.auth = HTTPBasicAuth(user, password)

    def run(self):
        while True:
            queues_info = self.get_metrics()
            for queue in queues_info:
                self.put_metric(queue)
            time.sleep(TIME_BETWEEN_CHECKS)

    def get_metrics(self):
        response = requests.get(
            self.url,
            auth=self.auth)
        if response.status_code == 200:
            return response.json()

    def put_metric(self, queue):
        queue_name = queue['name']
        if queue_name in self.interesting_queues:
            self.cloudwatch.put_metric_data(
                namespace=self.metric_namespace,
                name=self.queue_to_metric_name[queue_name],
                unit="Count", value=queue['messages']
            )

if __name__ == '__main__':
    Exporter().run()
