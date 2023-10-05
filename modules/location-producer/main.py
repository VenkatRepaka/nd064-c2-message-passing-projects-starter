import time
import json
import os
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc

from kafka import KafkaProducer
import logging

logging.basicConfig(level=logging.DEBUG)


TOPIC_NAME = "locations"
# TOPIC_NAME = os.environ["TOPIC_NAME"]
# KAFKA_SERVER = "localhost:56353"
KAFKA_SERVER = "0.tcp.in.ngrok.io:15464"
# KAFKA_SERVER = "host.docker.internal:55956"
# KAFKA_SERVER = "docker.for.mac.localhost:55956"
# KAFKA_SERVER = "kafka-service:17569"
# KAFKA_SERVER = "172.18.0.2:55956"
# KAFKA_SERVER = os.environ["KAFKA_SERVER"]
print(KAFKA_SERVER)
# KAFKA_SERVER = "0.tcp.in.ngrok.io:17569"


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def __init__(self):
        print("Initializing kafka producer")
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

    def Create(self, request, context):
        print("Received request")
        request_value = {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
        }
        print(request_value)
        print("Sending message")
        metadata = self.producer.send(
            TOPIC_NAME, json.dumps(request_value).encode("utf-8")
        ).get()
        print(metadata)
        self.producer.flush()
        print("Message sent successfully")
        return location_pb2.LocationMessage(**request_value)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)

print("Server starting on port 5005")
server.add_insecure_port("[::]:5005")
server.start()

try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)
