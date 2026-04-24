from typing import Any, Generator

from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': "broker:29092"})


def get_kafka_producer() -> Generator[Producer, Any, None]:
    yield producer
    producer.poll(0)


def flush_kafka_producer() -> int:
    return producer.flush()
