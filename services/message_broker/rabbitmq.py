"""RabbitMQ service."""
import os
import json
import pika

class RabbitMQ:
    """RabbitMQ Client."""
    def __init__(self):
        self.url = os.environ.get('RABBITMQ_URL')
        self.exchange = os.environ.get('COGNITIVE_CLOSE_STAGE_EXC')
        self.queue = os.environ.get('RABBITMQ_QUEUE')
        self.connection = None
        self.channel = None
        self.connect()

    def connect(self):
        """Connect to RabbitMQ."""
        self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange, exchange_type='direct')
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.queue_bind(exchange=self.exchange, queue=self.queue)

    def publish(self, message):
        """Publish a message to the queue."""
        self.channel.basic_publish(exchange=self.exchange, routing_key=self.queue, body=json.dumps(message),)


    def close(self):
        """Close the connection."""
        self.channel.close()
        self.connection.close()