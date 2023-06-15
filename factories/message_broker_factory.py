"""Message Broker Factory"""
import os
from services.message_broker.azure_service_bus import AzureServiceBus
from services.message_broker.rabbitmq import RabbitMQ
from services.message_broker.amazon_sns import AmazonSNS


message_broker = {
    "aws": AmazonSNS,
    "azure": AzureServiceBus,
    "rabbitmq": RabbitMQ
}

class MessageBrokerFactory:
    """Message Broker Factory Class"""
    def create_message_broker(self):
        """Create message broker."""
        message_broker_impl = os.environ.get("MESSAGE_BROKER_IMPL", "rabbitmq")
        return message_broker[message_broker_impl]()
