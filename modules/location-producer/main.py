import time
import json
import os
from concurrent import futures

import grpc
import location_pb2
import location_pb2_grpc

from kafka import KafkaProducer


TOPIC_NAME = os.environ["TOPIC_NAME"]
# KAFKA_SERVER = "localhost:55956"
KAFKA_SERVER = os.environ["KAFKA_SERVER"]
print(KAFKA_SERVER)
# KAFKA_SERVER = "0.tcp.in.ngrok.io:17569"


class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def __init__(self):
        print("Initializing kafka producer")
        self.producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

    def Create(self, request, context):
        request_value = {
            "person_id": request.person_id,
            "longitude": request.longitude,
            "latitude": request.latitude,
        }
        print(request_value)
        self.producer.send(TOPIC_NAME, json.dumps(request_value).encode("utf-8"))
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
