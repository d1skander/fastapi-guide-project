from sqladmin import Admin, ModelView
from sqladmin.fields import file_display_formatter

from wtforms.fields import FileField#gemini подсказал

from models.users import UserModel as us
from models.users import UserModel as rw
from models.sight import SightModel as st
from models.sight import SightPicture as st_picture
from models.info import InfoModel as inf
from models.info import InfoPicture as inf_picture

from .admin_auth import AdminAuth

from core.config import CookieConfig


import itsdangerous


def admin_setup(app, engine):
    cookie_config = CookieConfig()
    authentication_backend = AdminAuth(secret_key=cookie_config.admin_secret_key.get_secret_value())
    admin = Admin(app, 
                  engine,
                  authentication_backend=authentication_backend)


    class UserAdmin(ModelView, model=us):
        column_list = [us.id, us.password, us.review, us.username]


    class ReviewAdmin(ModelView, model=rw):
        column_list = [rw.username, rw.review, rw.password, rw.id]


    class SightAdmin(ModelView, model=st):
        column_list = [st.id, st.description, st.name, st.pictures]


    class SightPictureAdmin(ModelView, model=st_picture):
        column_list = [st_picture.id, st_picture.sight_id, st_picture.image, st_picture.sight]
        column_formatters = {st_picture.image: file_display_formatter}
        column_formatters_detail = {st_picture.image: file_display_formatter}

        form_overrides = {
                    'image': FileField
                }


    class InfoAdmin(ModelView, model=inf):
        column_list = [inf.id, inf.description, inf.pictures]


    class InfoPicturesAdmin(ModelView, model=inf_picture):
        column_list = [inf_picture.id, inf_picture.info_id, inf_picture.image]
        column_formatters = {inf_picture.image: file_display_formatter}
        column_formatters_detail = {inf_picture.image: file_display_formatter}

        form_overrides = {
            'image': FileField
        }

        form_columns = ["info", "image"]


    admin.add_view(UserAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(SightAdmin)
    admin.add_view(SightPictureAdmin)
    admin.add_view(InfoAdmin)
    admin.add_view(InfoPicturesAdmin)