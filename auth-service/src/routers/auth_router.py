from typing import Annotated

from fastapi import APIRouter, Depends
from starlette import status

from dtos.change_password_dto import ChangePasswordDTO
from dtos.login_account_dto import LoginDTO
from schemas.token_schema import TokenSchema
from schemas.user_schema import UserSchema
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", status_code=status.HTTP_200_OK, response_model=TokenSchema)
def login_user(
        service: Annotated[AuthService, Depends()],
        dto: LoginDTO,
):
    return service.login(dto)


@router.post("/change-password", status_code=status.HTTP_200_OK, response_model=UserSchema)
def change_password(
        service: Annotated[AuthService, Depends()],
        dto: ChangePasswordDTO,
):
    return service.change_password(dto)
