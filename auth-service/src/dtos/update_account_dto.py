from pydantic import Field

from config.extended_base_model import ExtendedBaseModel
from enums.gender import Gender


class UpdateAccountDTO(ExtendedBaseModel):
    # tag: str = Field(min_length=1, max_length=32)
    # email: EmailStr
    # role: Role = Field(default=Role.USER)
    # password: str = Field(min_length=6, max_length=128)

    full_name: str = Field(min_length=1, max_length=32)
    gender: Gender
    description: str = Field(max_length=128)
    age: int = Field(ge=13, le=125)
