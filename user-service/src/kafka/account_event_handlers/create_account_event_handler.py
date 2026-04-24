from kafka.event_handler import EventHandler
from sqlalchemy.orm import Session

from dtos.create_account_dto import CreateAccountDTO
from services.user_service import UserService


class CreateAccountEventHandler(EventHandler):

    def __init__(self, session: Session):
        self.user_service = UserService(session)

    def run(self, message: bytes) -> None:
        create_account_dto = CreateAccountDTO.model_validate_json(message)
        self.user_service.create_user(create_account_dto)
