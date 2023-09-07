import os
from dataclasses import dataclass
from kafka import KafkaConsumer

@dataclass
class ConsumerConfig:
    """a Dataclass for storing our producer configs"""
    bootstrap_servers = os.getenv("REDPANDA_BROKERS", "")
    topic = "greetings"
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
                print(f"Consumed record. key={msg.key}, value={msg.value}")
        except:
            print(f"Could not consume from topic: {self.topic}")
            raise
            
config=ConsumerConfig()
consumer=Consumer(config)
consumer.consume()