from pydantic import Field

from config.kafka.schemas.base_event_schema import BaseEventSchema
from schemas.account_created_event_schema import AccountCreatedEventSchema


class UserEventSchema(BaseEventSchema):
    data: AccountCreatedEventSchema = Field()