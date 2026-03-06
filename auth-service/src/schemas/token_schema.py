from email.policy import default

from pydantic import Field

from config.extended_base_model import ExtendedBaseModel


class TokenSchema(ExtendedBaseModel):
    access_token: str
    refresh_token: str = Field(default="TODO: Implement refresh token")
    token_type: str