from typing_extensions import Self

from pydantic import BaseModel, model_validator, Field


class UserModel(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=20)
    password_repeat: str = Field(min_length=8, max_length=20, exclude=True)

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')
        return self


class UserAuthModel(BaseModel):
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8, max_length=20)