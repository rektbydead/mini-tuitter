from typing import Annotated

from confluent_kafka import Producer
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from config.database_session import get_session
from crypto.auth.jwt_handler import JWTHandler
from crypto.hashing_context import HashingContext
from dtos.change_password_dto import ChangePasswordDTO
from dtos.login_account_dto import LoginDTO
from dtos.register_account_dto import RegisterAccountDTO
from kafka.kafka_producer import get_kafka_producer
from models.entity.user_entity import AuthUserEntity
from schemas.account_created_event_schema import AccountCreatedEventSchema
from schemas.jwt_data_schema import JwtDataSchema
from schemas.token_schema import TokenSchema


class AuthService:

    def __init__(self, session: Annotated[Session, Depends(get_session)],
                 producer: Annotated[Producer, Depends(get_kafka_producer)]) -> None:
        self._session = session
        self._producer = producer

    def register(self, dto: RegisterAccountDTO) -> AuthUserEntity:
        entity = AuthUserEntity(
            email=dto.email.__str__(),
            hashed_password=HashingContext.generate_hash(dto.password),
        )

        self._session.add(entity)
        self._session.flush([entity])
        self._session.refresh(entity)

        self._producer.produce(
            'account-created',
            AccountCreatedEventSchema(
                id=entity.id,
                tag=dto.tag,
                role=dto.role,
                full_name=dto.full_name,
                gender=dto.gender,
                description=dto.description,
                country='Portugal',
                age=dto.age,
                created_at=entity.created_at,
                updated_at=entity.updated_at,
            ).model_dump_json()
        )

        return entity

    def login(self, dto: LoginDTO) -> TokenSchema:
        user_entity = self.get_user_by_email(dto.email.__str__())
        jwt_data = JwtDataSchema(id=user_entity.id)
        access_token = JWTHandler.generate_token(jwt_data)
        return TokenSchema(access_token=access_token, token_type="Bearer")

    def change_password(self, dto: ChangePasswordDTO) -> AuthUserEntity:
        user_entity = self.get_user_by_email(dto.email.__str__())

        if HashingContext.verify_password(dto.old_password, user_entity.hashed_password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password is not correct")

        user_entity.hashed_password = HashingContext.generate_hash(dto.new_password)

        self._session.add(user_entity)
        self._session.flush([user_entity])
        self._session.refresh(user_entity)

        return user_entity

    def get_user_by_email(self, email: str) -> AuthUserEntity:
        user = self._session.query(AuthUserEntity).where(AuthUserEntity.email == email).scalar()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user
