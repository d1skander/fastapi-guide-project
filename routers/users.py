from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import select, update

from typing import Annotated

from forms.users import UserForm, UserAuthForm, UserEditUsernameForm, UserEditPasswordForm

from shemas.users import UserModel as UserShema
from shemas.users import UserAuthModel as UserAuthShema

from core.dependencies import DB, CHECK_COOKIE, HAVE_COOKIE, OPTIONAL_SESSION
from core.config import JWTConfig

from models.users import UserModel


import bcrypt
import jwt


router = APIRouter(prefix="/users", tags=["Пользователи"])

jwt_config = JWTConfig()


templates = Jinja2Templates(directory="templates")

#Регистрация
@router.get("/registration")
def get_registration_page(request: Request,
                          have_cookie: OPTIONAL_SESSION):
    if have_cookie is not None:
        return RedirectResponse(request.url_for("get_main_page"),
                                        status_code=303)
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
        stmt = db.execute(select(UserModel).where(UserModel.username == data.username)).scalar_one_or_none()
        if stmt is None:
            new_data = UserModel(username=data.username,
                             password=data.password)
            db.add(new_data)
            db.commit()
            return RedirectResponse(request.url_for("get_auth_page"), status_code=201)
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "Username is taken"}, status_code=400)
    except ValueError:
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "Value error, Passwords do not match"}, status_code=400)

#Авторизация
@router.get("/auth")
def get_auth_page(request: Request,
                  have_cookie: OPTIONAL_SESSION):
    if have_cookie is not None:
        return RedirectResponse(request.url_for("get_main_page"),
                                                status_code=303)
    form = UserAuthForm()
    return templates.TemplateResponse(name='users/auth.html', request=request, context={"form": form})

@router.post("/auth")
def auth_user(username: Annotated[str, Form(min_length=3, max_length=20)],
              password: Annotated[str, Form(min_length=8, max_length=20)],
              request: Request,
              db: DB):
    try:
        data = UserAuthShema(username=username, 
                             password=password)
        stmt = select(UserModel).where(UserModel.username == data.username)
        user = db.execute(stmt).scalar_one_or_none()
        if user is not None:
            if bcrypt.checkpw(data.password.encode("utf-8"), user.password.encode("utf-8")):
                jwt_token = jwt.encode({"id": str(user.id)}, jwt_config.key.get_secret_value(), jwt_config.algorithm.get_secret_value())
                redirect_to_profile = RedirectResponse(request.url_for("get_main_page"),
                                                       status_code=303)
                redirect_to_profile.set_cookie(key="key", 
                                    value=jwt_token,
                                    max_age=86400,
                                    secure=True,
                                    httponly=True,
                                    samesite='lax')
                return redirect_to_profile
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "User not found"}, status_code=404)
    except ValueError:
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "Incorrect login or password"}, status_code=400)

#Профиль
@router.get("/profile")
def get_profile_page(request: Request,
                     db: DB,
                     cookie: CHECK_COOKIE,
                     have_cookie: HAVE_COOKIE):
    user = db.execute(select(UserModel).where(UserModel.id == cookie)).scalar_one_or_none()
    user_form = UserEditUsernameForm()
    password_form = UserEditPasswordForm()
    if user is None:
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "not found"}, status_code=404)
    return templates.TemplateResponse(name='users/profile.html', request=request, context={"username": user.username, 
                                                                                           "id": str(user.id),
                                                                                           "user_form": user_form,
                                                                                           "password_form": password_form})

#Новый логин
@router.post("/new_username")
def new_username(username: Annotated[str, Form(min_length=3, max_length=20)],
                 db: DB,
                 cookie: CHECK_COOKIE,
                 request: Request):
    from shemas.users import UserEditUsernameModel as UEUShema
    valid_username = UEUShema(username=username)
    stmt = db.execute(select(UserModel).where(UserModel.username == valid_username.username)).scalar_one_or_none()
    if stmt is None:
        stmt = update(UserModel).where(UserModel.id == cookie).values(username=valid_username.username)
        new_user = db.execute(stmt)
        db.commit()
        return RedirectResponse(request.url_for("get_profile_page"),
                                status_code=303)
    return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "Username is taken"}, status_code=400)

#Новый пароль
@router.post("/new_password")
def new_password(password: Annotated[str, Form(min_length=8, max_length=20)],
                 db: DB,
                 cookie: CHECK_COOKIE,
                 request: Request):
    from shemas.users import UserEditPasswordModel as UEPShema
    valid_password = UEPShema(password=password)
    stmt = update(UserModel).where(UserModel.id == cookie).values(password=valid_password.password)
    new_password = db.execute(stmt)
    db.commit()
    return RedirectResponse(request.url_for("get_profile_page"),
                            status_code=303)

#Выход из сессии
@router.post("/logout")
def logout(request: Request):
    response = RedirectResponse(request.url_for("get_main_page"),
                            status_code=303)
    response.delete_cookie("key")
    return response