"""Amazon SNS message broker."""
import os
import json
import boto3

class AmazonSNS:
    """Amazon SNS message broker."""
    def __init__(self):
        self.client = boto3.client(
            'sns',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name=os.environ.get('AWS_REGION'),
        )

    def publish(self, message):
        """Publish a message to the topic."""
        self.client.publish(
            TopicArn=os.environ.get('AWS_SNS_TOPIC_ARN'),
            Message=json.dumps(message),
        )  