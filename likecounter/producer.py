from confluent_kafka import Producer
import json
import os
import time

conf = {'bootstrap.servers' : 'localhost:9092'}
producer = Producer(**conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_likes_event(post_id):
    producer.produce(
        'likes_topics',
        key=str(post_id),
        value=json.dumps({"post_id": post_id}),
        callback=delivery_report
    )
    print("Sent to Kafka")
    producer.flush()  

