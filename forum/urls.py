from django.contrib import admin
from django.urls import path, include

from .views import create_question, show_question


app_name = 'forum'
urlpatterns = [
    path('create_question/', create_question, name='create_question'),
    path('@<int:question_id>/', show_question, name='show_question'),
]