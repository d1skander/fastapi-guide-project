from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import select

from fastapi import Depends, Cookie, Request
from fastapi.responses import RedirectResponse

from typing import Annotated, Any

from db.database import engine

from models.users import UserModel


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    with SessionLocal() as db:
        yield db

#Зависимость для обращения в базу данных.
DB = Annotated[Session, Depends(get_db)]


def check_cookie_and_get_current_user(request: Request,
                 db: DB):
    from routers.users import templates

    import jwt

    visit = Cookie()
    if visit != None:
        try:
            payload = jwt.decode(visit)
            id = payload.get("id")
            token_data = str(id)
            if id is None:
                return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "problem in jwt"}, status_code=401)
            token_data = str(id)
        except jwt.InvalidTokenError:
            return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "problem in jwt"}, status_code=401)
        stmt = select(UserModel).where(UserModel.id == token_data)
        result = db.execute(stmt).scalar_one_or_none()
        if result is None:
            return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "problem in find"}, status_code=401)
        return result.id
    else:
        return RedirectResponse(request.url_for("auth"), status_code=201)


def get_active_user(current: Annotated[UserModel, Depends(check_cookie_and_get_current_user)]):
    if not current:
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "no active"}, status_code=401)
    return current


CURRENT = Annotated[str, Depends(get_active_user)]