from config.extended_base_model import ExtendedBaseModel


class TokenDataSchema(ExtendedBaseModel):
    user: str | None = None