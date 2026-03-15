from datetime import datetime
from typing import Optional

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from models.base_entity import BaseEntity
from enums.gender import Gender
from enums.role import Role


class UserEntity(BaseEntity):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    tag: Mapped[str] = mapped_column(unique=True, index=True)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.USER)

    full_name: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)

    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)
    updated_at: Mapped[Optional[datetime]] = mapped_column(default=datetime.now(), nullable=True)
