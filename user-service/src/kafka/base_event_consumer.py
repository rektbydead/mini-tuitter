import abc
import logging
import signal
from pathlib import Path
from typing import Generator

from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField


class BaseEventConsumer(abc.ABC):

    def __init__(self, group_id: str, events: list[str], schema_file_name: str) -> None:
        self.__logger__ = logging.getLogger(__name__)

        self.__initialize_serializer(
            schema_file_name=schema_file_name
        )

        self.__initialize_consumers(
            group_id=group_id,
            events=events
        )

        signal.signal(signal.SIGTERM, self.shutdown_consumer)
        signal.signal(signal.SIGINT, self.shutdown_consumer)

    def __initialize_serializer(self, schema_file_name: str) -> None:
        self.__schema_registry_client = SchemaRegistryClient({
            'url': 'http://schema-registry:8081'
        })

        self.__avro_deserializer = AvroDeserializer(
            self.__schema_registry_client,
            self.__load_schema(schema_file_name),
            lambda obj, ctx: obj
        )

        self.__logger__.info(f"Loading '{schema_file_name}' schema.")

    def __initialize_consumers(self, group_id: str, events: list[str]) -> None:
        self.__consumer = Consumer({
            'bootstrap.servers': 'broker:29092',
            'group.id': group_id,
        })

        self.__consumer.subscribe(events)
        self.__logger__.info(f"Subscribed to topic(s) {", ".join(events)}, waiting for messages...")

    @classmethod
    def __load_schema(cls, name: str) -> str:
        base = Path(__file__).parent.parent
        path = base / 'contracts' / name
        return path.read_text()

    def shutdown_consumer(self, sig=None, frame=None):
        self.__logger__.info("Shutting down kafka consumer...")
        self.__consumer.close()


    @abc.abstractmethod
    def handle_message(self, message: dict) -> None:
        ...

    def initialize(self) -> None:
        for message in self.__consume():
            self.handle_message(message=message)

    def __consume(self) -> Generator[dict, None, None]:
        while True:
            message = self.__consumer.poll(timeout=1)

            if message is None:
                continue

            if message.error():
                self.__logger__.error("Consumer error: %s", message.error())
                continue

            message_value = self.__avro_deserializer(
                message.value(),
                SerializationContext(message.topic(), MessageField.VALUE)
            )

            if message_value is None:
                continue

            self.__logger__.info(f"Received message: {message_value}")

            yield message_value
