from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import UUID, String, Numeric, CheckConstraint, ForeignKey, VARCHAR
from sqlalchemy.dialects.postgresql import ENUM

from models.base import Base


import uuid

#Модель пользователя
class User(Base):
    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(VARCHAR(20), nullable=False)
    password: Mapped[str] = mapped_column(String(300))

#Модель отзывов
class ReviewModel(Base):
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sight = models.ForeignKey(SightModel, on_delete=models.CASCADE)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(validators=[verification_number_reviews])
    description = models.TextField(default="Описание отсутсвует.", max_length=500)