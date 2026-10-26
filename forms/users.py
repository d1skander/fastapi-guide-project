from wtforms import StringField, PasswordField, Form, validators


class UserForm(Form):
    username = StringField('Имя пользователя', 
                           [validators.Length(min=3, max=20)], 
                           name="username")
    password = PasswordField('Новый пароль', [
        validators.Length(min=3, max=20),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли должны совпадать')],
        name="password")
    confirm = PasswordField('Повторите пароль', 
                            name="confirm")


class UserAuthForm(Form):
    username = StringField('Имя пользователя', 
                           [validators.Length(min=3, max=20)], 
                           name="username")
    password = PasswordField('Новый пароль', [
        validators.Length(min=3, max=20),
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Пароли должны совпадать')],
        name="password")