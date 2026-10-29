from sqladmin import Admin, ModelView

from .admin_auth import AdminAuth


def admin_setup(app, engine):
    authentication_backend = AdminAuth(secret_key="secret")
    admin = Admin(app, 
                  engine,
                  authentication_backend=authentication_backend)


    class UserAdmin(ModelView):
        pass


    class ReviewAdmin(ModelView):
        pass


    class SightAdmin(ModelView):
        pass


    class SightPictureAdmin(ModelView):
        pass


    admin.add_view(UserAdmin)
    admin.add_view(ReviewAdmin)
    admin.add_view(SightAdmin)
    admin.add_view(SightPictureAdmin)