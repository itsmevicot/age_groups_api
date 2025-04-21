import pika
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel
from app.config.settings import get_settings

_settings = get_settings()

class RabbitMQProvider:
    _conn: BlockingConnection | None = None
    _ch: BlockingChannel | None = None

    @classmethod
    def get_channel(cls) -> BlockingChannel:
        if cls._ch is None:
            params = pika.URLParameters(_settings.RABBIT_URI)
            cls._conn = pika.BlockingConnection(params)
            ch: BlockingChannel = cls._conn.channel()
            ch.queue_declare(queue=_settings.RABBIT_QUEUE_NAME, durable=True)
            cls._ch = ch
        return cls._ch

    @classmethod
    def close(cls) -> None:
        if cls._conn:
            cls._conn.close()
            cls._conn = None
            cls._ch = None
