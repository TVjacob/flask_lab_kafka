# kafka_producer.py
from confluent_kafka import Producer
import json

conf = {'bootstrap.servers': 'kafka1:9092,kafka2:9093,kafka3:9094,kafka4:9095'}
producer = Producer(**conf)

def emit_event(topic, data):
    message = json.dumps(data)
    producer.produce(topic, key=str(data.get('batch_id')), value=message)
    producer.flush()
