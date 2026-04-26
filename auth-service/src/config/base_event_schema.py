from datetime import datetime
from uuid import uuid4

from config.extended_base_model import ExtendedBaseModel
from pydantic import Field


class BaseEventSchema(ExtendedBaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: str = Field()
    created_at: datetime = Field(default_factory=datetime.now(datetime.UTC))
    version: int = Field(default=1)
    data: dict | None = Field(default_factory=lambda: None)
