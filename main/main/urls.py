"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', views.main, name="main"),
    path('sight/<uuid:id>', views.sight, name="sight"),
    path('info/', views.info, name="info"),
    path('auth/', views.auth, name="auth"),
    path('profile/', views.profile, name="profile"),
    path('registration/', views.registration, name="reg"),
    path('del_user/', views.delete_user, name="del"),
    path('edit_email/', views.edit_email, name='new_email'),
    path('edit_password/', views.edit_password, name='new_password'),
    path('edit_username/', views.edit_username, name='new_username'),
    path('exit/', views.exit, name='exit'),
]


# Source - https://stackoverflow.com/q/72418504
# Posted by TBS5596
# Retrieved 2026-11-19, License - CC BY-SA 4.0

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
