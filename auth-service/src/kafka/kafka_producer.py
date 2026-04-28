import logging
from pathlib import Path
from typing import Any, Generator

from confluent_kafka import Producer, SerializingProducer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer

logger = logging.getLogger(__name__)

def load_schema(name: str) -> str:
    base = Path(__file__).parent.parent
    path = base / 'contracts' / name
    logger.info(f"Loading schema from: {path.read_text()}")
    return path.read_text()


avro_serializer = AvroSerializer(
    SchemaRegistryClient({
        'url': 'http://schema-registry:8081'
    }),
    load_schema("account-events.avsc")
)

producer = SerializingProducer({
    'bootstrap.servers': "broker:29092",
    'key.serializer': lambda k, ctx: k.encode('utf-8'),
    'value.serializer': avro_serializer
})

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

def get_kafka_producer() -> Generator[Producer, Any, None]:
    try:
        yield producer
    except Exception as e:
        logger.info(f"Error: {e}")
    finally:
        producer.poll(0)


def flush_kafka_producer() -> int:
    return producer.flush()
