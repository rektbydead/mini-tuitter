from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from dtos.create_account_dto import CreateAccountDTO
from dtos.update_account_dto import UpdateAccountDTO
from schemas.user_schema import UserSchema
from services.user_service import UserService

router = APIRouter(prefix="", tags=["User"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserSchema)
def create_user(
        service: Annotated[UserService, Depends()],
        dto: CreateAccountDTO,
):
    return service.create_user(dto=dto)


@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
def update_user(
        user_id: int,
        service: Annotated[UserService, Depends()],
        dto: UpdateAccountDTO,
):
    return service.update_user(dto=dto, user_id=user_id)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
def get_user(
        user_id: int,
        service: Annotated[UserService, Depends()],
):
    return service.get_user_by_id(user_id=user_id)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserSchema)
def delete_user(
        user_id: int,
        service: Annotated[UserService, Depends()],
):
    return service.delete_user(user_id=user_id)
