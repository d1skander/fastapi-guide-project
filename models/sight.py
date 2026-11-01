from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import UUID, VARCHAR, Text, ForeignKey
from sqlalchemy_file import FileField

from models.base import Base

from typing import List


import uuid

#Модель достопримечательности
class SightModel(Base):
    __tablename__ = "sight"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(VARCHAR(), default="Название отсутствует.")
    description: Mapped[str] = mapped_column(Text())
    pictures: Mapped[List["Picture"]] = relationship()

#Дочерняя модель достопримечательности(Модель изображений)
class SightPicture(Base):
    __tablename__ = "sight_picture"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sight_id: Mapped[UUID] = mapped_column(ForeignKey("sight.id"))
    image = mapped_column(FileField)
