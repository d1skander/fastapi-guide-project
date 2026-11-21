from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import AbstractUser


import uuid


def verification_number_reviews(value: int):
    if value == 0 or value > 5:
        raise ValidationError(f"{value} <- does not fall within the 1–5 range")


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to="avatars_picture", default="default_picture/default.png")


class SightModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, default="Название отсутствует.")
    description = models.TextField(default="Описание отсутсвует.")
    image = models.ImageField(upload_to="sight_picture", default="default_picture/default.png")
    url_sight = models.URLField(max_length=200)


class ReviewModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sight = models.ForeignKey(SightModel, on_delete=models.CASCADE)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    grade = models.PositiveSmallIntegerField(validators=[verification_number_reviews])
    description = models.TextField(default="Описание отсутсвует.", max_length=500)


class InformationModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    description = models.TextField(default="Описание отсутсвует.", max_length=500)
    image = models.ImageField(upload_to="info_picture", default="default_picture/default.png")