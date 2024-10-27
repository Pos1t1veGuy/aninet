from django.contrib import admin
from django.urls import path, include

from .views import questions, create_question, show_question


app_name = 'forum'
urlpatterns = [
    path('', questions, name='questions'),
    path('create-question/', create_question, name='create_question'),
    path('q<int:question_id>/', show_question, name='show_question'),
]