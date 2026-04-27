import signal

from confluent_kafka import Consumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import SerializationContext, MessageField
from sqlalchemy.orm import Session

from config.database_session import session_context_manager
from config.logging import logger
from kafka.account_event_handlers.create_account_event_handler import CreateAccountEventHandler
from kafka.account_event_handlers.delete_account_event_handler import DeleteAccountEventHandler

bro = """
{
  "type": "record",
  "name": "AccountEvent",
  "namespace": "minituitter.authservice.account",
  "fields": [
    {
      "name": "event_id",
      "type": "string",
      "doc": "Unique id for the event"
    },
    {
      "name": "event_type",
      "type": {
        "type": "enum",
        "name": "AccountEventType",
        "symbols": [
          "CREATED",
          "UPDATED",
          "DELETED"
        ]
      }
    },
    {
      "name": "user_tag",
      "type": "string"
    },
    {
      "name": "timestamp",
      "type": "long",
      "doc": "Epoch millis"
    },
    {
      "name": "data",
      "type": [
        "null",
        {
          "type": "record",
          "name": "AccountData",
          "fields": [
            {
              "name": "name",
              "type": [
                "null",
                "string"
              ],
              "default": null
            },
            {
              "name": "email",
              "type": [
                "null",
                "string"
              ],
              "default": null
            }
          ]
        }
      ],
      "default": null
    }
  ]
}"""


class AccountEventConsumer:

    def __init__(self) -> None:
        logger.info('Initializing Kafka Consumer')

        schema_registry_client = SchemaRegistryClient({
            'url': 'http://schema-registry:8081'
        })

        self._avro_deserializer = AvroDeserializer(
            schema_registry_client,
            bro,
            lambda obj, ctx: obj
        )

        self.__consumer = Consumer({
            'bootstrap.servers': 'broker:29092',
            'group.id': 'user-service',
        })

        self.__consumer.subscribe([
            'AccountEvent',
            # 'account-updated',
            # 'account-deleted',
        ])

        logger.info("Subscribed to topic 'account-created', waiting for messages...")

        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def __handle_account_updated_topic(self, message) -> None:
        pass

    def __handle_account_delete_topic(self, message) -> None:
        pass

    def __distribute_handling(self, session: Session, topic: str | None, message: dict):
        pass
        # match topic:
        #     case 'account-created':
        #         CreateAccountEventHandler(session).run(message)
        #     case 'account-deleted':
        #         DeleteAccountEventHandler(session).run(message)
        #     case _:
        #         raise NotImplementedError(f'Handling of topic {topic} not implemented')

    def initialize(self) -> None:
        while True:
            logger.info("Waiting for message...")
            message = self.__consumer.poll(timeout=1)

            if message is None:
                continue

            if message.error():
                logger.error("Consumer error: %s", message.error())
                continue

            # message_value = self._avro_deserializer(message.value(), None) # message.value()
            message_value = self._avro_deserializer(
                message.value(),
                SerializationContext(message.topic(), MessageField.VALUE)
            )

            logger.info(f"message: {message_value}")

            if message_value is None:
                continue

            with session_context_manager() as session:
                try:
                    logger.info("Distributing received message (topic=%s): %s", message.topic(), message_value)
                    self.__distribute_handling(session, message.topic(), message_value)
                    logger.info("Message handled successfully (topic=%s): %s", message.topic(), message_value)
                except Exception as e:
                    logger.exception("Failed to process message with error and payload: %s - %s", e, message_value)

    def shutdown(self, sig=None, frame=None):
        logger.info("Shutting down kafka consumer...")
        self.__consumer.close()


if __name__ == "__main__":
    AccountEventConsumer().initialize()
