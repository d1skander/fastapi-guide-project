from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import aauthenticate, alogin, logout
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm, AuthForm

#Функция http-ошибок
def error_render(request, text: str, status: int):
    context = {"error": text, "status": status}
    return render(request=request, 
                  template_name="errors.html", 
                  context=context,
                  status=status)

#Авторизация
async def auth(request):
    if request.method == "POST":
        form = AuthForm(request.POST)
        if form.is_valid():
            user = await aauthenticate(username=form.cleaned_data.get("username"),
                                       password = form.cleaned_data.get("password"))
            if user is not None:
                await alogin(request, user)
                return redirect("main")
            else:
                return error_render(request, "invalid password or login", status=401)
    form = AuthForm()
    return render(request=request, 
                  template_name="users/auth.html",
                  context={"form": form})

#Регистрация
async def registration(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = await User.objects.acreate_user(username=form.cleaned_data.get("username"),
                                                   email=form.cleaned_data.get("main"),
                                                   password=form.cleaned_data.get("password"))
                authenticate_user = await aauthenticate(username=form.cleaned_data.get("username"),
                                              password=form.cleaned_data.get("password"))
                if authenticate_user is not None:
                    await alogin(request, user)
                    return redirect("main")
                else:
                    return redirect("auth")
            except IntegrityError:
                return error_render(request, "username taken", status=400)
    else:
        form = RegistrationForm()
        return render(request=request, template_name="users/registration.html", context={"form": form})

#Профиль
@login_required(redirect_field_name="auth")
async def profile(request):
    user = await request.auser()
    if user.is_authenticated:
        username = request.user.username
        mail = request.user.email
        return render(request=request, 
                      template_name="users/profile",
                      context={"username": username,
                               "mail": mail})
    return redirect('auth')

#Главная страница
def main(request):
    return render(request=request, template_name="main/main.html")

#Достопримечательность
def sight(request):
    return render(request=request, template_name="main/sight.html")

#Информация
def info(request):
    return render(request=request, template_name="main/info.html")