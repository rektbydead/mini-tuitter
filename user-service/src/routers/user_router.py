from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from dtos.update_account_dto import UpdateAccountDTO
from schemas.full_user_schema import UserSchema
from services.user_service import UserService

router = APIRouter(prefix="", tags=["User"])


@router.put(
    "/{user_tag}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema
)
def update_user(
        user_tag: str,
        service: Annotated[UserService, Depends()],
        dto: UpdateAccountDTO,
):
    return service.update_user(dto=dto, user_tag=user_tag)


@router.get(
    "/{user_tag}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema
)
def get_user(
        user_tag: str,
        service: Annotated[UserService, Depends()],
):
    return service.get_user_by_tag(user_tag=user_tag)


@router.delete(
    "/{user_tag}",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema
)
def delete_user(
        user_tag: str,
        service: Annotated[UserService, Depends()],
):
    return service.delete_user(user_tag=user_tag)
