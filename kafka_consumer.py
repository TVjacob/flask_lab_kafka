# kafka_consumer.py
from confluent_kafka import Consumer
import json

conf = {
    'bootstrap.servers': 'localhost:9092,localhost:9093,localhost:9094,localhost:9095',
    'group.id': 'lab_notifications',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(**conf)
consumer.subscribe(['customer_notification', 'audit_trail'])

def send_email_sms(batch_id, status, customer_id):
    print(f"[NOTIFY] Batch {batch_id} status: {status} -> notify customer {customer_id}")

while True:
    msg = consumer.poll(1.0)
    if msg is None:
        continue
    if msg.error():
        print("Consumer error: {}".format(msg.error()))
        continue

    data = json.loads(msg.value())
    if 'customer_id' in data:
        send_email_sms(data['batch_id'], data['status'], data['customer_id'])
    else:
        print(f"[AUDIT] {data}")
