from django import forms

#Регистрация
class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=3, 
                               max_length=20)
    password = forms.CharField(min_length=3, 
                               max_length=20,
                               widget=forms.PasswordInput)

#Авторизация
class AuthForm(forms.Form):
    username = forms.CharField(min_length=3,
                               max_length=20)
    password = forms.CharField(min_length=3, 
                               max_length=20,
                               widget=forms.PasswordInput)

#Смена логина
class EditUsernameForm(forms.Form):
    username = forms.CharField(
        label="Новый логин", 
        max_length=20, 
        min_length=3,
        widget=forms.TextInput
    )

#Смена почты
class EditEmailForm(forms.Form):
    email = forms.EmailField(
        label="Новая почта",
        widget=forms.EmailInput
    )

#Смена пароля
class EditPasswordForm(forms.Form):
    password = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput
    )
