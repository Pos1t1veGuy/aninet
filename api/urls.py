from django.contrib import admin
from django.urls import path, include

from .views import get_mail_msgs, get_videos, get_chat_msgs


app_name = 'api'
urlpatterns = [
    path('get/mail-messages', get_mail_msgs, name='info'),
    path('get/videos', get_videos, name='info'),
    path('get/chat-messages', get_chat_msgs, name='info'),
    #path('post/', post, name='post'),
]