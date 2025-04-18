"""
Queue sender module for publishing processed stock analysis to RabbitMQ or SQS.
"""

import json
import os

import boto3
import pika
from pika.exceptions import AMQPConnectionError

from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)

# Read queue type
QUEUE_TYPE = os.getenv("QUEUE_TYPE", "rabbitmq").lower()

# RabbitMQ settings
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_EXCHANGE = os.getenv("RABBITMQ_EXCHANGE", "stock_analysis")
RABBITMQ_ROUTING_KEY = os.getenv("RABBITMQ_ROUTING_KEY", "trend")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST", "/")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")

# SQS settings
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL", "")
SQS_REGION = os.getenv("SQS_REGION", "us-east-1")

# Initialize SQS client if needed
sqs_client = None
if QUEUE_TYPE == "sqs":
    try:
        sqs_client = boto3.client("sqs", region_name=SQS_REGION)
    except Exception as e:
        logger.error(f"Failed to initialize SQS client: {e}")


def publish_to_queue(messages: list[dict]) -> None:
    """
    Publishes a list of messages to the configured message queue.

    Args:
    ----
        messages (list[dict]): List of messages (each a dict) to be published.
    """
    if QUEUE_TYPE == "rabbitmq":
        _publish_to_rabbitmq(messages)
    elif QUEUE_TYPE == "sqs":
        _publish_to_sqs(messages)
    else:
        logger.error("Invalid QUEUE_TYPE specified. Must be 'rabbitmq' or 'sqs'.")


def _publish_to_rabbitmq(messages: list[dict]) -> None:
    """
    Internal method to publish messages to RabbitMQ.

    Args:
    ----
        messages (list[dict]): List of messages to send.
    """
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                virtual_host=RABBITMQ_VHOST,
                credentials=credentials,
            )
        )
        channel = connection.channel()
        channel.exchange_declare(exchange=RABBITMQ_EXCHANGE, exchange_type="topic", durable=True)

        for message in messages:
            channel.basic_publish(
                exchange=RABBITMQ_EXCHANGE,
                routing_key=RABBITMQ_ROUTING_KEY,
                body=json.dumps(message),
            )
            logger.info(f"Published message to RabbitMQ: {message}")

        connection.close()
    except AMQPConnectionError as e:
        logger.error(f"RabbitMQ connection error: {e}")
    except Exception as e:
        logger.error(f"Failed to publish to RabbitMQ: {e}")


def _publish_to_sqs(messages: list[dict]) -> None:
    """
    Internal method to publish messages to AWS SQS.

    Args:
    ----
        messages (list[dict]): List of messages to send.
    """
    if not sqs_client or not SQS_QUEUE_URL:
        logger.error("SQS client or queue URL not properly configured.")
        return

    for message in messages:
        try:
            response = sqs_client.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=json.dumps(message),
            )
            logger.info(f"Published message to SQS. MessageId: {response['MessageId']}")
        except Exception as e:
            logger.error(f"Failed to publish to SQS: {e}")
