from django.contrib import admin
from django.urls import path, include

from .views import mailbox, show_message


app_name = 'mail'
urlpatterns = [
    path('mail/', mailbox, name='mailbox'),
    path('mail/@<str:message_id>/', show_message, name='show_message'),
]