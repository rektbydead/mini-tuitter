from confluent_kafka import Consumer
from sqlalchemy.orm import Session

from config.database_session import get_engine, create_db_and_tables
from config.logging import logger
from dtos.create_account_dto import CreateAccountDTO
from services.user_service import UserService


def process_message(payload: bytes | None) -> None:
    with Session(get_engine()) as session:
        try:
            create_account_dto = CreateAccountDTO.model_validate_json(payload)
            logger.info("Processing account creation for: %s", create_account_dto)
            service = UserService(session)
            created_user = service.create_user(create_account_dto)
            session.commit()
            logger.info("Successfully created user for account: %s", created_user.tag)
        except Exception as e:
            session.rollback()
            logger.exception("Failed to process message with error and payload: %s - %s", e, payload)


def consume_messages():
    consumer = Consumer({
        'bootstrap.servers': 'broker:29092',
        'group.id': 'user-service',
    })

    consumer.subscribe(['account-created'])
    logger.info("Subscribed to topic 'account-created', waiting for messages...")

    while True:
        message = consumer.poll(1)

        if message is None:
            continue

        if message.error():
            logger.error("Consumer error: %s", message.error())
            continue

        logger.info("Received message (key=%s)", message.key())
        logger.debug("Message value: %s", message.value())
        process_message(payload=message.value())

    consumer.close()


if __name__ == "__main__":
    consume_messages()
