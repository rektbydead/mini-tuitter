from datetime import datetime
from typing import Optional

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from models.base_entity import BaseEntity
from enums.gender import Gender
from enums.role import Role


class AuthUserEntity(BaseEntity):
    __tablename__ = "auth_user_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    tag: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)
