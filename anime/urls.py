from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from .views import home, anime


app_name = 'anime'
urlpatterns = [
    path('', home, name='home'),
    path('anime/', anime, name='anime'),
]