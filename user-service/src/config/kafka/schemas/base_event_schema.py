import time
import uuid
from pydantic import Field

from config.extended_base_model import ExtendedBaseModel
from config.kafka.schemas.event_type import EventType


class BaseEventSchema(ExtendedBaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: EventType
    timestamp: int = Field(default_factory=lambda: int(time.time() * 1000))
    user_tag: str
    data: dict | None = Field(default=None)