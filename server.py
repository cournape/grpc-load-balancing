# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter server."""

import argparse
import logging
import random
import time

from concurrent import futures

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


logger = logging.getLogger(__name__)


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    def __init__(self, average, std):
        self._average = average
        self._std = std

    def SayHello(self, request, context):
        if self._std == 0:
            latency = self._average
        else:
            latency = random.normalvariate(self._average, self._std)
        logger.info("Sleeping for %.2f ms", latency * 1000)
        time.sleep(latency)
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve(average, std):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(average, std), server)
    host = "[::]:50051"
    server.add_insecure_port(host)
    logger.info("Starting server on host %s", host)
    server.start()
    server.wait_for_termination()


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "--latency-average", "-l", type=float, default=0.05,
        help="Average latency (in seconds)"
    )
    p.add_argument(
        "--latency-std", "-s", type=float, default=0.01,
        help="latency standard deviation (in seconds^sqrt(2))"
    )

    ns = p.parse_args()

    logging.basicConfig(level=logging.INFO)
    serve(ns.latency_average, ns.latency_std)


if __name__ == '__main__':
    main()
