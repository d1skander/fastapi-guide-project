from fastapi import APIRouter, Request, Form, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates

from sqlalchemy import select

from typing import Annotated

from forms.users import UserForm, UserAuthForm

from shemas.users import UserModel as UserShema
from shemas.users import UserAuthModel as UserAuthShema

from core.dependencies import DB, CURRENT
from core.config import CookieConfig, JWTConfig

from models.users import UserModel


import bcrypt
import jwt


router = APIRouter(prefix="/users", tags=["Пользователи"])

jwt_config = JWTConfig()


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
                     password_repeat=confirm)
        new_data = UserModel(username=data.username,
                             password=data.password)
        db.add(new_data)
        db.commit()
        return RedirectResponse(request.url_for("get_auth_user"), status_code=201)
    except ValueError:
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "Value error, Passwords do not match"}, status_code=400)

#Авторизация
@router.get("/auth")
def get_auth_page(request: Request):
    form = UserAuthForm()
    return templates.TemplateResponse(name='users/auth.html', request=request, context={"form": form})

@router.post("/auth")
def auth_user(username: Annotated[str, Form(min_length=3, max_length=20)],
              password: Annotated[str, Form(min_length=8, max_length=20)],
              request: Request,
              db: DB,
              response: Response):
    try:
        data = UserAuthShema(username=username, 
                             password=password)
        stmt = select(UserModel).where(UserModel.username == data.username)
        user = db.execute(stmt).scalar_one_or_none()
        if user is not None:
            if bcrypt.checkpw(data.password.encode("utf-8"), user.password.encode("utf-8")):
                jwt_token = jwt.encode({"id": user.id}, jwt_config.key, jwt_config.algorithm)
                response.set_cookie(key="key", 
                                    value=jwt_token,
                                    max_age=86400,
                                    secure=True,
                                    httponly=True,
                                    samesite='lax')
                return RedirectResponse(request.url_for("get_profile_page"), status_code=201)
    except ValueError:
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "Incorrect login or password"}, status_code=400)

#Профиль
@router.get("/profile")
def get_profile_page(request: Request,
                     current: CURRENT,
                     db: DB):
    user = db.execute(select(UserModel).where(UserModel.id == current)).scalar_one_or_none()
    if user is None:
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "not found"}, status_code=404)
    return templates.TemplateResponse(name='users/profile.html', request=request)