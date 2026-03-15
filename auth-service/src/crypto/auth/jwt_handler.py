from datetime import timedelta, datetime
from typing import Any

import jwt

from schemas.jwt_data_schema import JwtDataSchema

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = 30


class JWTHandler:

    @staticmethod
    def generate_token(data: JwtDataSchema):
        expire_data = datetime.now() + timedelta(hours=ACCESS_TOKEN_EXPIRE)
        jwt_data = data.model_dump() | {"exp": expire_data}

        return jwt.encode(
            jwt_data,
            SECRET_KEY,
            algorithm=ALGORITHM
        )

    @staticmethod
    def verify_token(self, token: str) -> dict[str, Any]:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
