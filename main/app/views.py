from django.shortcuts import render, redirect
from django.contrib.auth import aauthenticate, alogin, logout, get_user_model
from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings

from random import randint

from .forms import RegistrationForm, AuthForm, EditEmailForm, ReviewForm
from .forms import EditPasswordForm, EditUsernameForm, EmailCodeForm, EditAvatarProfile

from .models import SightModel, InformationModel, ReviewModel


User = get_user_model()

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


@login_required
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
    email_form = EditEmailForm()
    password_form = EditPasswordForm()
    username_form = EditUsernameForm()
    email_code_form = EmailCodeForm()
    avatar_form = EditAvatarProfile()
    user = await request.auser()
    if user.is_authenticated:
        username = user.username
        mail = user.email
        id = user.id
        image = user.image.url
        return render(request=request, 
                      template_name="users/profile.html",
                      context={"username": username,
                               "email": mail,
                               "id": id,
                               "image": image,
                               "email_form": email_form,
                               "password_form": password_form,
                               "username_form": username_form,
                               "email_code_form": email_code_form,
                               "avatar_form": avatar_form})
    return redirect("auth")

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

#Достопримечательность(Помог ИИ)
def sight(request, id):
    try:
        sight = SightModel.objects.get(id=id)
    except ObjectDoesNotExist:
        return error_render(request, "Not found", status=404)

    # Проверяем, оставлял ли текущий пользователь уже отзыв
    has_reviewed = False
    if request.user.is_authenticated:
        has_reviewed = ReviewModel.objects.filter(
            sight=sight, username=request.user
        ).exists()

    if request.method == "POST":
        # Если не авторизован или отзыв уже есть — не сохраняем
        if not request.user.is_authenticated or has_reviewed:
            return redirect("sight", id=sight.id)  # замените на имя вашего url

        form = ReviewForm(request.POST)
        if form.is_valid():
            r = ReviewModel.objects.create(
                username=request.user,
                sight=sight,
                description=form.cleaned_data["description"],
                grade=form.cleaned_data["grade"],
                )
            r.save()
            return redirect("sight", id=sight.id)  # защита от повторной отправки F5
    else:
        form = ReviewForm()
    reviews = ReviewModel.objects.filter(sight__id=id).all()
    return render(
        request=request,
        template_name="main/sight.html",
        context={
            "sight": sight,
            "form": form,
            "has_reviewed": has_reviewed,  # передаем в шаблон, чтобы скрыть форму
            "reviews": reviews
        },
    )

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
@login_required
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
            return redirect("profile")
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

#Новая почта(ИИ помог)
@login_required
def edit_email(request):
    from django.http import JsonResponse
    if request.method != "POST":
        return JsonResponse({"error": "Метод не разрешен"}, status=405)

    # ЭТАП 2: Пользователь отправил форму из <dialog id="codeEmailWindow">
    if "code" in request.POST:
        code_form = EmailCodeForm(request.POST)
        if not code_form.is_valid():
            return JsonResponse({"error": "Неверный формат кода"}, status=400)

        input_code = str(code_form.cleaned_data.get("code"))
        saved_code = request.session.get("email_verify_code")
        new_email = request.session.get("email_verify_address")

        if saved_code and new_email and input_code == str(saved_code):
            request.user.email = new_email
            request.user.save()
            
            # Очищаем временные данные из сессии
            del request.session["email_verify_code"]
            del request.session["email_verify_address"]
            
            return JsonResponse({"status": "ok", "message": "Почта успешно изменена"})
        else:
            return JsonResponse({"error": "Неверный код подтверждения"}, status=400)

    # ЭТАП 1: Пользователь отправил первую форму (с новым email)
    form = EditEmailForm(request.POST)
    if form.is_valid():
        new_email = form.cleaned_data.get("email")
        code = randint(1000, 9999)
        
        request.session["email_verify_code"] = code
        request.session["email_verify_address"] = new_email
        
        try:
            send_mail(
                subject="Код подтверждения",
                message=f"Ваш код: {code}",
                from_email=None,
                recipient_list=[new_email],
            )
            return JsonResponse({"status": "code_sent"})
        except BadHeaderError:
            return JsonResponse({"error": "Ошибка заголовка письма"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
            
    return JsonResponse({"error": "Некорректный email"}, status=400)
    

#Новый пароль
@login_required
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
            return redirect("profile")
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
@login_required
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

#Добавления изображения
@login_required
def edit_avatar(request):
    user = request.user
    if request.method == "POST":
        form = EditAvatarProfile(request.POST, request.FILES)
        if form.is_valid():
            new_image = form.cleaned_data.get("avatar")
            if new_image:
                user.image = new_image
                user.save()
            return redirect("profile")
        return redirect("profile")
    return redirect("profile")