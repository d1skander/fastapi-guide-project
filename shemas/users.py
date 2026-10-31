from typing_extensions import Self

from pydantic import BaseModel, model_validator, Field


import bcrypt
import uuid


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=20)
    password_repeat: str = Field(min_length=8, max_length=20, exclude=True)

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')
        return self


    @model_validator(mode='after')
    def hash_password(self) -> Self:
        hashed = bcrypt.hashpw(self.password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed.decode("utf-8")
        return self


class UserAuthModel(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=20)