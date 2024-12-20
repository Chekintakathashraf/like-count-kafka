# tracker/management/commands/consumer.py
from django.core.management.base import BaseCommand
from confluent_kafka import Consumer, KafkaException 
import json
from likes.models import Post
import os
import sys
from django.db import transaction
from collections import defaultdict
from likes.models import Post

class Command(BaseCommand):
    help = 'Run Kafka consumer to listen for likes updates'

    # def handle(self, *args, **options):
    #     conf = {
    #         'bootstrap.servers': "localhost:9092",
    #         'group.id': "likes_group",
    #         'auto.offset.reset': 'earliest'
    #     }

    #     consumer = Consumer(conf)
    #     consumer.subscribe(['likes_topics'])

    #     try:
    #         while True:
    #             msg = consumer.poll(timeout=1.0)
    #             if msg is None:
    #                 continue
    #             if msg.error():
    #                 if msg.error().code() == KafkaException._PARTITION_EOF:
    #                     continue
    #                 else:
    #                     print(msg.error())
    #                     break

    #             data = json.loads(msg.value().decode('utf-8'))
    #             post_id = data['post_id']
    #             print(f"Received and saved: {data}")

    #     except KeyboardInterrupt:
    #         pass
    #     finally:
    #         consumer.close()
    
    
    def process_batch(self,like_batch):

        with transaction.atomic():
            for post_id,like_count in like_batch.items():
                post = Post.objects.get(id=post_id)
                post.like += like_count
                post.save()
        
    def handle(self, *args, **options):
        print("** kafka started **")
        like_batch = defaultdict(int)
        conf = {
            'bootstrap.servers': "localhost:9092",
            'group.id': "likes_group",
            'auto.offset.reset': 'earliest'
        }

        consumer = Consumer(conf)
        consumer.subscribe(['likes_topics'])
        total_messages = 0

        try:
            while True:
                print("** listing for messages **")
                msg = consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaException._PARTITION_EOF:
                        continue
                    else:
                        print(msg.error())
                        break

                data = json.loads(msg.value().decode('utf-8'))
                post_id = data['post_id']
                like_batch[post_id] += 1
                print('like_batch = ',like_batch)
                print('total_messages = ',total_messages)
                total_messages += 1
                if total_messages >= 10:
                    self.process_batch(like_batch)
                    like_batch.clear()
                    total_messages = 0
                
                print(f"Received and saved: {data}")

        except KeyboardInterrupt:
            pass
        finally:
            consumer.close()
            
                
    
    
    
            