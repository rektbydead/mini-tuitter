from datetime import datetime

from pydantic import EmailStr

from config.extended_base_model import ExtendedBaseModel
from enums.gender import Gender


class UserSchema(ExtendedBaseModel):
    id: int

    tag: str
    email: EmailStr

    full_name: str
    gender: Gender
    description: str
    country: str
    age: int

    created_at: datetime
    updated_at: datetime
