"""menumaker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from mealdelivery.views import (home_page, user_logout, LoginView,
                                change_password, change_password_mandatory)

urlpatterns = [
    path(
        '',
        home_page,
        name='home'),
    path(
        'admin/',
        admin.site.urls),
    path(
        'delivery/',
        include('mealdelivery.urls')),
    path(
        'user_login/',
        LoginView.as_view(),
        name='user_login'),
    path(
        'logout/',
        user_logout,
        name='logout'),
    path(
        'password/',
        change_password,
        name='change_password'),
    path(
        'password2/',
        change_password_mandatory,
        name='change_password2'),
    path(
        'accounts/password_reset/',
        auth_views.PasswordResetView.as_view(),
        name='password_reset'),
    path(
        'accounts/password_reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'),
    path(
        'accounts/reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'),
    path(
        'accounts/reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT)
