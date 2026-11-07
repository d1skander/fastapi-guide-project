from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select

from fastapi import Depends, Cookie, HTTPException
from fastapi.responses import RedirectResponse

from typing import Annotated, Any

from db.database import engine

from models.users import UserModel

from core.config import JWTConfig


import jwt


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Any:
    with SessionLocal() as db:
        yield db

#Зависимость для обращения в базу данных.
DB = Annotated[Session, Depends(get_db)]


def check_cookie(jwt_cookie: Annotated[str | None, Cookie(alias="key")] = None) -> str:
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
         raise ValueError("invalid token")

#Просмотр сессий(куки)
CHECK_COOKIE = Annotated[str, Depends(check_cookie)]


def have_cookie(cookie: Annotated[str | None, Cookie(alias="key")] = None) -> str:
    if not cookie:
        raise HTTPException(status_code=401)
    return cookie
        
#Проверка сессии, где нужна авторизация
HAVE_COOKIE = Annotated[bool, Depends(have_cookie)]


def get_optional_cookie(cookie: Annotated[str | None, Cookie(alias="key")] = None) -> str | None:
    return cookie

# Зависимость для гостевых страниц
OPTIONAL_SESSION = Annotated[str | None, Depends(get_optional_cookie)]
