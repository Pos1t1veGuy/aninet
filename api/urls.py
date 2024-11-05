from django.contrib import admin
from django.urls import path, include

from .views import get_mail_msgs, get_videos, get_chat_msgs, post_user_theme, get_animes


app_name = 'api'
urlpatterns = [
    path('get/mail-messages', get_mail_msgs, name='get_mail_msgs'),
    path('get/videos', get_videos, name='get_videos'),
    path('get/chat-messages', get_chat_msgs, name='get_chat_msgs'),
    path('get/animes', get_animes, name='get_animes'),
    path('post/theme', post_user_theme, name='post_user_theme'),
]