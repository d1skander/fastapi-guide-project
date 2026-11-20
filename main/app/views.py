from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import aauthenticate, alogin, logout
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .forms import RegistrationForm, AuthForm, EditEmailForm, EditPasswordForm, EditUsernameForm
from .models import SightModel, InformationModel

#Функция http-ошибок
def error_render(request, text: str, status: int):
    context = {"error": text, "status": status}
    return render(request=request, 
                  template_name="errors.html", 
                  context=context,
                  status=status)

#Авторизация
async def auth(request):
    user = await request.auser()
    if user.is_authenticated:
        return redirect("profile")
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


@login_required(redirect_field_name="auth")
def exit(request):
    logout(request)
    return redirect("auth")


#Регистрация
async def registration(request):
    user = await request.auser()
    if user.is_authenticated:
        return redirect("profile")
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
                return error_render(request, 
                                    "username taken", 
                                    status=400)
    else:
        form = RegistrationForm()
        return render(request=request, 
                      template_name="users/registration.html", 
                      context={"form": form})

#Профиль
async def profile(request):
    user = await request.auser()
    if user.is_authenticated:
        username = user.username
        mail = user.email
        id = user.id
        return render(request=request, 
                      template_name="users/profile.html",
                      context={"username": username,
                               "email": mail,
                               "id": id})

#Главная страница
def main(request):
    try:
        sights = SightModel.objects.all()
        return render(request=request, 
                    template_name="main/main.html",
                    context={"form": sights})
    except ObjectDoesNotExist:
        return error_render(request, 
                            "Not found", 
                            status=500)

#Достопримечательность
def sight(request, id):
    try:
        sight = SightModel.objects.get(id=id)
        if request.method == 'POST':
            return render(request=request, 
                      template_name='main/sight.html', 
                      context={"sight": sight})
        
        return render(request=request, 
                    template_name='main/sight.html', 
                    context={"sight": sight})
    except ObjectDoesNotExist:
        return error_render(request, 
                            "Not found", 
                            status=500)

#Информация
def info(request):
    try:
        info = InformationModel.objects.all()
        return render(request=request, 
                    template_name="main/info.html",
                    context={"form": info})
    except ObjectDoesNotExist:
        return error_render(request, 
                            "Not found", 
                            status=500)

#Новый логин
def edit_username(request):
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        
        # Принимаем и валидируем форму
        form = EditUsernameForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data.get("username")
            user.username = new_username
            user.save()
            
            resp = HttpResponse()
            resp.status_code = 204
            return redirect("main")
        else:
            return error_render(request, 
                                "No correct username", 
                                status=400)
            
    except User.DoesNotExist:
        return error_render(request, 
                            "DoesNotExist", 
                            status=404)
    except Exception as e:
        return error_render(request, 
                            "Error", 
                            status=500)

#Новая почта
def edit_email(request):
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        form = EditEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data.get("email") 
            user.email = new_email
            user.save()
            
            resp = HttpResponse()
            resp.status_code = 204
            return redirect("main")
        else:
            return error_render(request, 
                                "No correct mail", 
                                status=400)
            
    except User.DoesNotExist:
        return error_render(request, 
                            "DoesNotExist", 
                            status=404)
    except Exception as e:
        return error_render(request, 
                            "Error", 
                            status=500)
    

#Новый пароль
def edit_password(request):
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        form = EditPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get("password") 
            user.set_password(password)
            user.save()
            
            resp = HttpResponse()
            resp.status_code = 204
            return resp
        else:
            return error_render(request, 
                                "No correct password", 
                                status=400)
                        
    except User.DoesNotExist:
        return error_render(request, 
                            "DoesNotExist", 
                            status=404)
    except Exception as e:
        return error_render(request, 
                            "Error", 
                            status=500)

#Удаление профиля
def delete_user(request):
    try:
        username = request.user.username
        user = User.objects.get(username=username)
        user.delete()
        resp = HttpResponse()
        resp.status_code = 204
        return redirect("main")
    except User.DoesNotExist:
        return error_render(request, 
                            "DoesNotExist", 
                            status=404)
    except Exception as e:
        return error_render(request, 
                            "Error", 
                            status=500)