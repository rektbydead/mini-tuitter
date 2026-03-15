from confluent_kafka import Consumer
from fastapi import Depends
from sqlalchemy.sql.annotation import Annotated

from dtos.create_account_dto import CreateAccountDTO
from services.user_service import UserService

service = Annotated[UserService, Depends()]

consumer = Consumer({
    'bootstrap.servers': 'broker:29092'
})

consumer.subscribe(['account-created'])

def process_message(message):
    create_account_dto = CreateAccountDTO(**message)
    pass

while True:
    message = consumer.poll(1)

    if message is None:
        continue

    if message.error():
        print("Consumer error: {}".format(message.error()))
        continue

    print(f"Received message ({message.key()}): {message}")
    process_message(message)



consumer.close()