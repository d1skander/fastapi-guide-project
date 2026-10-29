from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from typing import Annotated

from forms.users import UserForm, UserAuthForm

from shemas.users import UserModel as UserShema
from shemas.users import UserAuthModel as UserAuthShema


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
                      request: Request):
    print(username, password, confirm)
    try:
        data = UserShema(username=username, 
                     password=password, 
                     password_repeat=confirm)
        print(data)
        return True#RedirectResponse(request.url_for("main"), status_code=201)
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
              request: Request):
    print(username, password)
    try:
        data = UserAuthShema(username=username, 
                             password=password)
        print(data)
        return True#RedirectResponse(request.url_for("main"), status_code=201)
    except ValueError:
        return templates.TemplateResponse(name='errors.html', request=request, context={"errors": "Incorrect login or password"}, status_code=400)

#Профиль
@router.get("/profile")
def get_profile_page(request: Request):
    return templates.TemplateResponse(name='users/profile.html', request=request)