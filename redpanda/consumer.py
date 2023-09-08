import os
from dataclasses import dataclass
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

cloud_id = "My_deployment:dXMtY2V..."
username = "elastic"
password = "PWD"
data_stream_name = "logs-news.currents-default"
es = Elasticsearch(
    cloud_id=cloud_id,
    basic_auth=(username, password),
)
def index_to_elastcisearch(es=es,datastream=data_stream_name,document={}):
    if document!={}:
        try:
        # Index the document to the data stream
                document["published"]=document["published"].split(" +")[0]
                response = es.index(index=datastream, body=document)
                print("Document indexed successfully:")
                print(response)
        except Exception as e:
                print("Error indexing document:")
                print(e) 
    else:
        print("Nothing to do here!")

@dataclass
class ConsumerConfig:
    """a Dataclass for storing our producer configs"""
    bootstrap_servers = os.getenv("REDPANDA_BROKERS", "localhost:9092")
    topic = "News"
    consumer_group = "my-group"
    auto_offset_reset = "earliest"

class Consumer:
    def __init__(self, config:ConsumerConfig) -> None:
        self.client=KafkaConsumer(
            config.topic,
            bootstrap_servers=config.bootstrap_servers,
            group_id=config.consumer_group,
            auto_offset_reset=config.auto_offset_reset
        )
        self.topic=config.topic

    def consume(self):
        try:
            for msg in self.client:
                #print(f"Consumed record. key={msg.key}, value={msg.value}")
                index_to_elastcisearch(document=json.loads((msg.value.decode())))
        except:
            print(f"Could not consume from topic: {self.topic}")
            raise
            
config=ConsumerConfig()
consumer=Consumer(config)
consumer.consume()