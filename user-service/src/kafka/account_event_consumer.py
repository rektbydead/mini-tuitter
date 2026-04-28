from config.logging import logger
from kafka.account_event_handlers.create_account_event_handler import CreateAccountEventHandler
from kafka.account_event_handlers.delete_account_event_handler import DeleteAccountEventHandler
from kafka.base_event_consumer import BaseEventConsumer

from config.database_session import session_context_manager


class AccountEventConsumer(BaseEventConsumer):

    def __init__(self) -> None:
        super().__init__(
            group_id='user-service',
            events=['AccountEvent'],
            schema_file_name='account-events.avsc'
        )

    def handle_message(self, message: dict):
        self.__logger__.info(f"Received Data: {message['data']}")

        with session_context_manager() as session:
            match message['event_type']:
                case 'CREATED':
                    CreateAccountEventHandler(session).run(message['data'])
                case _:
                    raise NotImplementedError(f'Handling of event_type {message['event_type']} not implemented')


if __name__ == "__main__":
    AccountEventConsumer().initialize()
