from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy import UUID, VARCHAR, Text, ForeignKey
from sqlalchemy_imageattach.entity import Image, image_attachment

from models.base import Base

from typing import List


import uuid


class SightModel(Base):
    __tablename__ = "sight"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(VARCHAR(), default="Название отсутствует.")
    description: Mapped[str] = mapped_column(Text())
    picture: Mapped[List["Picture"]] = image_attachment("SightPicture")


class SightPicture(Base, Image):
    __tablename__ = "sight_picture"
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sight_id: Mapped[UUID] = mapped_column(ForeignKey("sight.id"))
