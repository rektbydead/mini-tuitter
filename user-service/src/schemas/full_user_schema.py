from config.extended_base_model import ExtendedBaseModel


class UserSchema(ExtendedBaseModel):
    tag: str

    full_name: str
    country: str
    description: str
    age: int
