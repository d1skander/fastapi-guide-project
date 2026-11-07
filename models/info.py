from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import UUID, VARCHAR, Text, ForeignKey
from sqlalchemy_file.types import FileField

from models.base import Base

from typing import List


import uuid

#Модель информации
class InfoModel(Base):
    __tablename__ = "info"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description: Mapped[str] = mapped_column(Text())
    pictures: Mapped[List["Picture"]] = relationship("SightPicture")

#Дочерняя модель информации(Модель изображений)
class InfoPicture(Base):
    __tablename__ = "info_picture"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    info_id: Mapped[UUID] = mapped_column(ForeignKey("info.id"))
    image = mapped_column(FileField)