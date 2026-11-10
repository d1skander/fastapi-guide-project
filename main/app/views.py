from django.shortcuts import render

#Авторизация
def auth(request):
    return render(request=request, template_name="users/auth.html")

#Регистрация
def registration(request):
    return render(request=request, template_name="users/registration.html")

#Профиль
def profile(request):
    return render(request=request, template_name="users/profile")

#Главная страница
def main(request):
    return render(request=request, template_name="main/main.html")

#Достопримечательность
def sight(request):
    return render(request=request, template_name="main/sight.html")

#Информация
def info(request):
    return render(request=request, template_name="main/info.html")