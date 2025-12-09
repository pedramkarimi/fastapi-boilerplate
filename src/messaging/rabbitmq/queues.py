# src/messaging/queues.py

from dataclasses import dataclass
from pika.adapters.blocking_connection import BlockingChannel

WELCOME_EMAIL_QUEUE = "email.welcome"

# بعداً می‌تونی این‌ها رو اضافه کنی:
# RESET_PASSWORD_QUEUE = "email.reset_password"
# OTP_SMS_QUEUE = "sms.otp"
# WEEKLY_REPORT_QUEUE = "report.weekly"
# ...

@dataclass(frozen=True)
class QueueConfig:
    name: str
    durable: bool = True

WELCOME_EMAIL_QUEUE_CONFIG = QueueConfig(name=WELCOME_EMAIL_QUEUE)


def declare_welcome_email_queue(channel: BlockingChannel) -> None:
    channel.queue_declare(
        queue=WELCOME_EMAIL_QUEUE_CONFIG.name,
        durable=WELCOME_EMAIL_QUEUE_CONFIG.durable,
    )
