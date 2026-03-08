from pydantic import Field, EmailStr, field_validator

from config.extended_base_model import ExtendedBaseModel
from enums.gender import Gender
from enums.role import Role


class RegisterAccountDTO(ExtendedBaseModel):
    tag: str = Field(min_length=1, max_length=32)
    email: EmailStr
    role: Role = Field(default=Role.USER)
    password: str = Field(min_length=6, max_length=128)

    full_name: str = Field(min_length=1, max_length=32)
    gender: Gender = Field(default=Gender.OTHERS)
    description: str = Field(max_length=128)
    age: int = Field(ge=13, le=125)

    @field_validator('password', mode='before')
    def validate_password(cls, password: str) -> str:
        """
        TODO: Must have numbers and capitalized letters.
        """
        return password
