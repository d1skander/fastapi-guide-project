from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import SightModel, ReviewModel, InformationModel


User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(SightModel)
admin.site.register(InformationModel)
admin.site.register(ReviewModel)
admin.site.register(User, UserAdmin)