from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select

from fastapi import Depends, Cookie, Request
from fastapi.responses import RedirectResponse

from typing import Annotated

from db.database import engine

from models.users import UserModel

from core.config import JWTConfig


import jwt


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db

#Зависимость для обращения в базу данных.
DB = Annotated[Session, Depends(get_db)]


def check_cookie(jwt_cookie: Annotated[str | None, Cookie(alias="key")] = None):
    if jwt_cookie is None:
        raise ValueError("Cookie missing")
    jwt_config = JWTConfig()
    try:
        payload = jwt.decode(jwt_cookie,
                             jwt_config.key.get_secret_value(),
                             [jwt_config.algorithm.get_secret_value()])
        jwt_id = payload.get("id")
        if jwt_id is None:
            raise ValueError("problem in find")
        return str(jwt_id)
    except jwt.InvalidTokenError:
         raise ValueError("problem in find")

#Просмотр сессий(куки)
CHECK_COOKIE = Annotated[str, Depends(check_cookie)]