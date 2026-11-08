from fastapi import APIRouter, Request, Form, Response, Cookie
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from typing import Annotated

from forms.users import UserForm, UserAuthForm, UserEditUsernameForm, UserEditPasswordForm

from shemas.users import UserModel as UserShema
from shemas.users import UserAuthModel as UserAuthShema

from core.dependencies import DB, CHECK_COOKIE, HAVE_COOKIE, OPTIONAL_SESSION, check_cookie
from core.config import JWTConfig

from models.users import UserModel
from models.info import InfoModel


import bcrypt
import jwt


router = APIRouter(prefix="/main", tags=["Основные маршруты"])

jwt_config = JWTConfig()


templates = Jinja2Templates(directory="templates")


@router.get("/main")
def get_main_page(request: Request,
                  have_cookie: OPTIONAL_SESSION,
                  db: DB):
    if have_cookie is not None:
        try:
            payload = jwt.decode(str(have_cookie),
                                 jwt_config.key.get_secret_value(),
                                 [jwt_config.algorithm.get_secret_value()])
            jwt_id = payload.get("id")
            if jwt_id is None:
                return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "problem in find"}, status_code=400)
            return templates.TemplateResponse(name='main/main.html', request=request, context={"state": True})
        except jwt.InvalidTokenError:
            return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "invalid token"}, status_code=400)
    else:
        return templates.TemplateResponse(name='main/main.html', request=request, context={"state": False})

#не долелал
@router.get("/info")
def get_info_page(request: Request,
                  db: DB):
       stmt = select(InfoModel).options(joinedload(InfoModel.pictures))
       info = db.scalars(stmt).first()
       return templates.TemplateResponse(name='main/info.html', request=request, context={"info": info})