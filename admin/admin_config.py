from sqladmin import Admin, ModelView
from sqladmin.fields import file_display_formatter

from models.users import UserModel as us
from models.users import UserModel as rw
from models.sight import SightModel as st
from models.sight import SightPicture as st_picture

from .admin_auth import AdminAuth


def admin_setup(app, engine):
    authentication_backend = AdminAuth(secret_key="secret")
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
        column_list = [st_picture.id, st_picture.sight_id, st_picture.image]
        column_formatters = {st_picture.image: file_display_formatter}
        column_formatters_detail = {st_picture.image: file_display_formatter}


    admin.add_view(UserAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(SightAdmin)
    admin.add_view(SightPictureAdmin)