from dataclasses import dataclass
import os, sys
import requests, json
from kafka import KafkaProducer

@dataclass
class ProducerConfig:
    """a Dataclass for storing our producer configs"""
    bootstrap_servers = os.getenv("REDPANDA_BROKERS", "localhost:9092")
    topic = "News"

class Producer:
    def __init__(self, config: ProducerConfig) -> None:
        self.client=KafkaProducer(
           bootstrap_servers=config.bootstrap_servers,
           key_serializer=str.encode,
           value_serializer=lambda m: json.dumps(m).encode("utf-8")
        )
        self.topic=config.topic

    def produce(self,message: str):
        try:
            future=self.client.send(self.topic,key="key1",value=message)
            _ = future.get(timeout=10)
            print(f"Successfully produced message to topic: {self.topic}")

        except:
            print(f"Could not produce to topic: {self.topic}")
            raise

config = ProducerConfig()
producer=Producer(config)
'''
with open("response.json","r") as f:
        content=f.read()
        dic=json.loads(content)
        for n in dic["news"]:
            producer.produce(n)

'''

topic=str(sys.argv[1])
url = ('https://api.currentsapi.services/v1/search?'
        'keywords='+topic+'&language=en&'
        'apiKey=API_TOKEN')
response = requests.get(url)   
print("======================")
print(response)
print("======================")
news=response.json()["news"] 
for new in news:
    producer.produce(new)


