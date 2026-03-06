from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from config.database_session import get_session
from crypto.auth.jwt_handler import JWTHandler
from crypto.hashing_context import HashingContext
from dtos.change_password_dto import ChangePasswordDTO
from dtos.login_account_dto import LoginDTO
from models.entity.user_entity import UserEntity
from schemas.jwt_data_schema import JwtDataSchema
from schemas.token_schema import TokenSchema
from services.user_service import UserService


class AuthService:

    def __init__(self, session: Annotated[Session, Depends(get_session)],
                 user_service: Annotated[UserService, Depends()]) -> None:
        self._session = session
        self._user_service = user_service

    def login(self, dto: LoginDTO) -> TokenSchema:
        user_entity = self._user_service.get_user_by_email(dto.email.__str__())
        jwt_data = JwtDataSchema(id=user_entity.id)
        access_token = JWTHandler.generate_token(jwt_data)
        return TokenSchema(access_token=access_token, token_type="Bearer")

    def change_password(self, dto: ChangePasswordDTO) -> UserEntity:
        user_entity = self._user_service.get_user_by_email(dto.email.__str__())

        if HashingContext.verify_password(dto.old_password, user_entity.hashed_password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password is not correct")

        user_entity.hashed_password = HashingContext.generate_hash(dto.new_password)

        self._session.add(user_entity)
        self._session.flush([user_entity])
        self._session.refresh(user_entity)

        return user_entity
