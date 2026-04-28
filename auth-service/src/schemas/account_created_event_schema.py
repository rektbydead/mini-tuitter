from datetime import datetime

from pydantic import Field, ConfigDict

from config.extended_base_model import ExtendedBaseModel
from enums.gender import Gender
from enums.role import Role


class AccountCreatedEventSchema(ExtendedBaseModel):
    model_config = ConfigDict(use_enum_values=True)

    tag: str = Field(min_length=1, max_length=32)
    role: Role = Field(default=Role.USER)
    full_name: str = Field(min_length=1, max_length=32)
    gender: Gender = Field(default=Gender.OTHERS)
    description: str = Field(max_length=128)
    country: str = Field(default="Portugal")
    age: int = Field(ge=13, le=125)
