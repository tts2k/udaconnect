import json
import os

from kafka import KafkaProducer

KAFKA_URL = os.getenv("KAFKA_URL", "localhost:9092")

def send_location_to_kafka(data):
    producer = KafkaProducer(bootstrap_servers=[KAFKA_URL])
    kafka_data = json.dumps(data).encode('utf-8')
    producer.send("update_location", kafka_data)
    producer.flush()
