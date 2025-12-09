import json
from typing import Any
from .connection import get_rabbitmq_connection
from .queues import declare_welcome_email_queue, WELCOME_EMAIL_QUEUE
from .schemas import WelcomeEmailMessage
import pika
from src.core.config import settings


def get_rabbitmq_connection() -> pika.BlockingConnection:
    credentials = pika.PlainCredentials(
        username=settings.RABBITMQ_USER,
        password=settings.RABBITMQ_PASSWORD,
    )

    parameters = pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=credentials,
        heartbeat=600,
        blocked_connection_timeout=300,
    )
    return pika.BlockingConnection(parameters)

def publish_welcome_email(message: WelcomeEmailMessage) -> None:
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # مطمئن می‌شیم queue وجود دارد (همان نام)
    # channel.queue_declare(
    #     queue=settings.WELCOME_EMAIL_QUEUE,
    #     durable=True,
    # )

    declare_welcome_email_queue(channel)

    body_dict: dict[str, Any] = message.model_dump()
    body_bytes: bytes = json.dumps(body_dict).encode("utf-8")

    channel.basic_publish(
        exchange="",
        routing_key=settings.WELCOME_EMAIL_QUEUE,
        body=body_bytes,
    )

    connection.close()
