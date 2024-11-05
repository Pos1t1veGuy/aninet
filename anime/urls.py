from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

from .views import home, animelist, anime, anime_episode


app_name = 'anime'
urlpatterns = [
    path('', home, name='home'),
    path('anime/', animelist, name='list'),
    path('anime/<str:slug>/', anime, name='anime'),
    path('anime/<str:slug>/<int:episode>/', anime_episode, name='anime_episode'),
]