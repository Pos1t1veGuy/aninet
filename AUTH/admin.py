from django.contrib import admin
from .models import User, Message

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'avatar']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['content', 'author', 'created_at', 'to']
