from django.contrib import admin
from django.urls import path,include
from . import views as home_views

urlpatterns = [
    path('', home_views.home_view, name='home'),
    path("users/",include('users.urls')),
    path("menu/",include('menu.urls')),
]