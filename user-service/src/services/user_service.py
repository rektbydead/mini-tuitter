from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from config.database_session import get_session
from crypto.hashing_context import HashingContext
from dtos.create_account_dto import CreateAccountDTO
from dtos.update_account_dto import UpdateAccountDTO
from models.entity.user_entity import UserEntity


class UserService:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self._session = session

    def create_user(self, dto: CreateAccountDTO) -> UserEntity:
        entity = UserEntity(
            email=dto.email.__str__(),
            tag=dto.tag,
            hashed_password=HashingContext.generate_hash(dto.password),
            full_name=dto.full_name,
            gender=dto.gender,
            description=dto.description,
            country="Portugal",  # TODO: Use geo location
            age=dto.age,
        )

        self._session.add(entity)
        self._session.flush([entity])
        self._session.refresh(entity)

        return entity

    def get_user_by_email(self, email: str) -> UserEntity:
        user = self._session.query(UserEntity).where(UserEntity.email == email).scalar()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    def get_user_by_id(self, user_id: int) -> UserEntity:
        user = self._session.query(UserEntity).where(UserEntity.id == user_id).scalar()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    def update_user(self, user_id: int, dto: UpdateAccountDTO) -> UserEntity:
        user_entity = self.get_user_by_id(user_id)

        user_entity.full_name = dto.full_name
        user_entity.gender = dto.gender
        user_entity.age = dto.age

        self._session.add(user_entity)
        self._session.flush([user_entity])
        self._session.refresh(user_entity)

        return user_entity

    def delete_user(self, user_id: int) -> UserEntity:
        user_entity = self.get_user_by_id(user_id)

        self._session.delete(user_entity)
        self._session.flush([user_entity])

        return user_entity
