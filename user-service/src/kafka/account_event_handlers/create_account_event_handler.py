import logging

from kafka.event_handler import EventHandler
from services.user_service import UserService
from sqlalchemy.orm import Session

from dtos.create_account_dto import CreateAccountDTO


class CreateAccountEventHandler(EventHandler):

    def __init__(self, session: Session):
        self.user_service = UserService(session)

    def run(self, message: bytes) -> None:
        logging.info(f"Entrou aqui carago: {message}")
        create_account_dto = CreateAccountDTO.model_validate(message)
        self.user_service.create_user(create_account_dto)
