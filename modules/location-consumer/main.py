import json
import os
from kafka import KafkaConsumer

# TOPIC_NAME = os.environ["TOPIC_NAME"]
# KAFKA_SERVER = os.environ["KAFKA_SERVER"]
KAFKA_SERVER = "0.tcp.in.ngrok.io:17569"

TOPIC_NAME = "locations"
# KAFKA_SERVER = "localhost:55956"

print(KAFKA_SERVER)

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)

for location in consumer:
    # print(location)
    message = location.value.decode("utf-8")
    print("{}".format(message))
    location_message = json.loads(message)
    print("Received message successfully")
