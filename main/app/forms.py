from PIL import Image, ImageOps, UnidentifiedImageError
from django import forms
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile, UploadedFile


import io
import uuid

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


class ReviewForm(forms.Form):
    from .models import verification_number_reviews
    description = forms.CharField(label="Текст", help_text="Посетили это место? Расскажите о своих впечатлениях!", widget=forms.Textarea)
    grade = forms.IntegerField(label="Оценка", help_text="Оцените это место от 1 до 5!", validators=[verification_number_reviews])

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

#Код потверждения почты
class EmailCodeForm(forms.Form):
    code = forms.IntegerField(
        min_value=1000,
        max_value=9999,
        label="Код потверждения",
        help_text="Код отправлен на почту"
    )

#Смена пароля
class EditPasswordForm(forms.Form):
    password = forms.CharField(
        min_length=3, 
        max_length=20,
        label="Новый пароль",
        widget=forms.PasswordInput
    )

#Написа ИИ
Image.MAX_IMAGE_PIXELS = 4096 * 4096
MAX_SIZE = 10 * 1024 * 1024


def normalize_image(file) -> InMemoryUploadedFile:
    if file.size > MAX_SIZE:
        raise ValidationError("Файл больше 10 МБ.")

    try:
        file.seek(0)
        with Image.open(file) as img:
            img = ImageOps.exif_transpose(img)
            img = img.convert("RGBA" if "A" in img.getbands() else "RGB")
            img = ImageOps.fit(img, (300, 300), Image.Resampling.LANCZOS)

            buf = io.BytesIO()
            img.save(buf, format="WEBP", quality=85)
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        raise ValidationError("Некорректное или повреждённое изображение.")

    return InMemoryUploadedFile(
        buf, "avatar", f"{uuid.uuid4().hex}.webp", "image/webp", buf.tell(), None
    )


class EditAvatarProfile(forms.Form):
    avatar = forms.ImageField(label="Аватар")

    #Написал ИИ
    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        return normalize_image(avatar) if isinstance(avatar, UploadedFile) else avatar