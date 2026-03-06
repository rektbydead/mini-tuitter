from pydantic import EmailStr

from config.extended_base_model import ExtendedBaseModel


class LoginDTO(ExtendedBaseModel):
    email: EmailStr
    password: str
