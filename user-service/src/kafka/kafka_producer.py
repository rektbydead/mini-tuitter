import logging
from pathlib import Path
from typing import Any, Generator

from anyio.functools import lru_cache
from confluent_kafka import Producer, SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry._sync.avro import AvroSerializer


def get_logger() -> logging.Logger:
    return logging.getLogger(__name__)


@lru_cache(maxsize=1)
def __get_producer() -> Producer:
    return SerializingProducer({
        'bootstrap.servers': "broker:29092",
        'key.serializer': lambda k, ctx: k.encode('utf-8'),
        'value.serializer': avro_serializer
    })

def load_schema(name: str) -> str:
    base = Path(__file__).parent.parent
    path = base / 'contracts' / name
    return path.read_text()


avro_serializer = AvroSerializer(
    SchemaRegistryClient({
        'url': 'http://schema-registry:8081'
    }),
    load_schema("account-events.avsc")
)


def get_producer() -> Generator[Producer, Any, None]:
    producer = __get_producer()

    try:
        yield producer
    except Exception as e:
        get_logger().error(e)
        raise
    finally:
        producer.poll(0)


def flush_producer() -> None:
    producer = __get_producer()
    producer.flush()