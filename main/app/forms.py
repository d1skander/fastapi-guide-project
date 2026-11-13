from django import forms

#Регистрация
class RegistrationForm(forms.Form):
    username = forms.CharField(min_length=3, 
                               max_length=20)
    mail = forms.EmailField(min_length=5, 
                            max_length=254)
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