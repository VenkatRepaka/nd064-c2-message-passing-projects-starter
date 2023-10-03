import json
import os
from kafka import KafkaConsumer

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_SERVER)

for location in consumer:
    message = location.value.decode("utf-8")
    print("{}".format(message))
    location_message = json.loads(message)
    print(location_message)
