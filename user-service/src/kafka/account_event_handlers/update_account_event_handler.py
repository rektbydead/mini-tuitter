import json

from sqlalchemy.orm import Session

from kafka.event_handler import EventHandler
from services.user_service import UserService


class DeleteAccountEventHandler(EventHandler):

    def __init__(self, session: Session):
        self.user_service = UserService(session)

    def run(self, message: bytes) -> None:
        loaded_message = json.loads(message)
        self.user_service.delete_user(loaded_message['id'])
