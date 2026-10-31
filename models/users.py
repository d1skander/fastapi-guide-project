from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import UUID, String, ForeignKey, VARCHAR, SmallInteger

from models.base import Base

from typing import List


import uuid

#Модель пользователя
class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    password: Mapped[str] = mapped_column(String(300))
    review: Mapped[List["Reviews"]] = relationship()

#Модель отзывов
class ReviewModel(Base):
    __tablename__ = "reviews"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    grade: Mapped[int] = mapped_column(SmallInteger())
    description: Mapped[str] = mapped_column(String(length=3000))

    @validates("grade")
    def scheck_grade(self, key: str, value: int) -> int:
        if not value <= 0 and not value > 5:
            return value
        else:
            raise ValueError("Your number is not within the required range")