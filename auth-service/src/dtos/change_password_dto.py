from pydantic import Field, EmailStr, field_validator

from config.extended_base_model import ExtendedBaseModel


class ChangePasswordDTO(ExtendedBaseModel):
    email: EmailStr
    old_password: str
    new_password: str = Field(min_length=6, max_length=128)

    @field_validator('new_password', mode='before')
    def validate_new_password(cls, new_password: str) -> str:
        """
        TODO: Must have numbers and capitalized letters.
        """
        return new_password
