from django.db import models
from django.contrib.auth.models import AbstractUser
from asgiref.sync import sync_to_async
from django.utils import timezone as tz

from django.conf import settings

from typing import *

import os


class ModelUtils:
    def filename(name: str) -> str:
        result_name = name
        count = 0

        while os.path.exists(result_name):
            filename, ext = '.'.join(result_name.split('.')[:-1]), result_name.split('.')[-1]

            if len(filename.split('_')):
                if filename.split('_')[-1].isdigit():
                    count = int(filename.split('_')[-1])+1
                    filename = '_'.join(filename.split('_')[:-1])
            
            result_name = f'{filename}_{count}.{ext}'
        
        return result_name
    
    def avatar_filename(instance, filename: str) -> str:
        return ModelUtils.filename(f'{settings.AVATARS_URL}{filename}')


class User(AbstractUser):
    username = models.CharField(max_length=settings.MAX_USERNAME_LENGTH, unique=True)
    email = models.EmailField(unique=True, verbose_name='email')
    avatar = models.ImageField(upload_to=ModelUtils.avatar_filename, default=settings.DEFAULT_AVATAR_URL, verbose_name='Avatar Picture')
    date_created = models.DateTimeField(default=tz.now, editable=False, verbose_name='Create Time')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Last Update')
    is_dark_theme = models.BooleanField(default=True, verbose_name='Default User Theme')

    def save(self, *args, **kwargs):
        if self.id:
            old_user = User.objects.get(pk=self.id)

            if old_user.avatar.url != self.avatar.url and old_user.avatar.url != settings.DEFAULT_AVATAR_URL:
                old_user.avatar.delete()

        super(User, self).save(*args, **kwargs)


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', verbose_name='Author')
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(default=tz.now, editable=False, verbose_name='Create Time')
    to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies', max_length=settings.MAX_USERNAME_LENGTH, default=None, null=True, verbose_name='Replies')

    def __str__(self):
        return f'Message(from="{self.author.username}", content="{self.content}", date_sent={self.date_sent})'