from fastapi import APIRouter, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from sqlalchemy import select

from typing import Annotated

from forms.users import UserForm, UserAuthForm

from shemas.users import UserModel as UserShema
from shemas.users import UserAuthModel as UserAuthShema

from core.dependencies import DB
from core.config import CookieConfig, JWTConfig

from models.users import UserModel


import bcrypt
import jwt


router = APIRouter(prefix="/users", tags=["Пользователи"])


templates = Jinja2Templates(directory="templates")

#Регистрация
@router.get("/registration")
def get_registration_page(request: Request):
    form = UserForm()
    return templates.TemplateResponse(name='users/registration.html', request=request, context={"form": form})

@router.post("/registration")
def registration_user(username: Annotated[str, Form(min_length=3, max_length=20)],
                      password: Annotated[str, Form(min_length=8, max_length=20)],
                      confirm: Annotated[str, Form(min_length=8, max_length=20)],
                      request: Request,
                      db: DB):
    try:
        data = UserShema(username=username, 
                     password=password, 
                     password_repeat=confirm).model_dump()
        db.add(**data)
        db.commit()
        return RedirectResponse(request.url_for("auth"), status_code=201)
    except ValueError:
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "Value error, Passwords do not match"}, status_code=400)

#Авторизация
@router.get("/auth")
def get_auth_page(request: Request,
                  db: DB):
    form = UserAuthForm()
    return templates.TemplateResponse(name='users/auth.html', request=request, context={"form": form})

@router.post("/auth")
def auth_user(username: Annotated[str, Form(min_length=3, max_length=20)],
              password: Annotated[str, Form(min_length=8, max_length=20)],
              request: Request,
              db: DB,
              config: JWTConfig,
              response: Response):
    try:
        data = UserAuthShema(username=username, 
                             password=password)
        stmt = select(UserModel).where(UserModel.username == data.username)
        user = db.execute(stmt).scalar_one_or_none()
        if user is not None:
            if bcrypt.checkpw(data.password.encode("utf-8"), user.password.encode("utf-8")):
                jwt_token = jwt.encode({"id": user.id}, config.key, config.algorithms)
                response.set_cookie(key="key", 
                                    value=jwt_token,
                                    max_age=86400,
                                    secure=True,
                                    httponly=True,
                                    samesite='lax')
                return RedirectResponse(request.url_for("main"), status_code=201)
    except ValueError:
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "Incorrect login or password"}, status_code=400)

#Профиль
@router.get("/profile")
def get_profile_page(request: Request):
    return templates.TemplateResponse(name='users/profile.html', request=request)