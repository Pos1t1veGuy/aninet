from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from .views import home, animelist, anime, anime_episode


app_name = 'anime'
urlpatterns = [
    path('', home, name='home'),
    path('anime/', animelist, name='animelist'),
    path('anime/<str:anime_name>/', anime, name='anime'),
    path('anime/<str:anime_name>/<int:episode>/', anime_episode, name='anime_episode'),
]