from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
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
    
    def preview_filename(instance, filename: str) -> str:
        return ModelUtils.filename(f'{settings.PREVIEW_URL}{filename}')
    
    def video_filename(instance, filename: str) -> str:
        return ModelUtils.filename(f'{settings.VIDEO_URL}{filename}')


class Anime(models.Model):
    name = models.CharField(max_length=100, unique=True)
    preview = models.ImageField(upload_to=ModelUtils.preview_filename, verbose_name='Preview')
    release_date = models.DateTimeField(verbose_name='Create Time', default=tz.now)
    views = models.PositiveBigIntegerField(verbose_name='Views Count', default=0)
    about = models.TextField(verbose_name='About', default='')
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='anime_viewed', verbose_name='Viewers', blank=True)

    def save(self, *args, **kwargs):
        if self.id:
            old_user = User.objects.get(pk=self.id)

            if self.preview and old_user.preview != self.preview:
                old_user.preview.delete()

        super(Anime, self).save(*args, **kwargs)

    def __str__(self):
        return f'Anime(name={self.name}, release_date={self.release_date}, views={self.views})'

class Episode(models.Model):
    name = models.CharField(max_length=100)
    anime = models.ForeignKey(Anime, related_name='episodes', verbose_name='Anime', on_delete=models.CASCADE)
    preview = models.ImageField(upload_to=ModelUtils.preview_filename, verbose_name='Preview')
    release_date = models.DateTimeField(verbose_name='Create Time', default=tz.now)
    released = models.BooleanField(verbose_name='Is Released', default=False)
    views = models.PositiveBigIntegerField(verbose_name='Views Count', default=0)
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='episodes_viewed', verbose_name='Viewers', blank=True)

    def save(self, *args, **kwargs):
        if self.id:
            old_user = User.objects.get(pk=self.id)

            if self.preview and old_user.preview != self.preview:
                old_user.preview.delete()

        super(Anime, self).save(*args, **kwargs)

    def __str__(self):
        return f'Episode(name={self.name}, release_date={self.release_date}, views={self.views}, released={self.released})'

class Dub(models.Model):
    author = models.CharField(max_length=100)
    episode = models.ForeignKey(Episode, related_name='dubs', verbose_name='Episode', on_delete=models.CASCADE)
    preview = models.ImageField(upload_to=ModelUtils.preview_filename, verbose_name='Preview')
    date_loaded = models.DateTimeField(default=tz.now, verbose_name='Create Time')
    views = models.PositiveBigIntegerField(verbose_name='Views Count', default=0)
    viewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dubs_viewed', verbose_name='Viewers', blank=True)
    video = models.FileField(upload_to=ModelUtils.video_filename, verbose_name='Video Content', null=True, blank=True, validators=[
		FileExtensionValidator(allowed_extensions=['mp4'])
	])
    op_start = models.PositiveSmallIntegerField(verbose_name='Openning Start Timing', default=0)
    op_end = models.PositiveSmallIntegerField(verbose_name='Openning End Timing', default=0)
    ending_start = models.PositiveSmallIntegerField(verbose_name='Endning Start Timing', default=0)

    def save(self, *args, **kwargs):
        if self.id:
            old_user = User.objects.get(pk=self.id)

            if self.preview and old_user.preview != self.preview:
                old_user.preview.delete()

        super(Anime, self).save(*args, **kwargs)

    def __str__(self):
        return f'Dub(author={self.author}, date_loaded={self.date_loaded}, views={self.views}, episode={self.episode.name}, episode.anime={self.episode.anime.name})'

class Grade(models.Model):
    anime = models.ForeignKey(Anime, related_name='grades', verbose_name='Anime', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='grades', verbose_name='Author', on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(verbose_name='Grade 0-5', validators=[MinValueValidator(0), MaxValueValidator(5)])

    def __str__(self):
        return f'Grade(user={self.user}, anime={self.anime.name}, value={self.value})'

class Comment(models.Model):
    episode = models.ForeignKey(Episode, related_name='comments', verbose_name='Episode', on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Content')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comments', verbose_name='Author', on_delete=models.CASCADE)
    date_sent = models.DateTimeField(default=tz.now, editable=False, verbose_name='Create Time')

    def __str__(self):
        return f'Comment(author={self.author}, episode={self.episode.name}, episode.anime={self.episode.anime.name}, content={self.content}, date_sent={self.date_sent})'

class Tag(models.Model):
    user = models.CharField(max_length=100)
    anime = models.ForeignKey(Anime, related_name='tags', verbose_name='Anime', on_delete=models.CASCADE)
    content = models.CharField(max_length=50)

    def __str__(self):
        return f'Tag(user={self.user}, anime={self.anime.name}, content={self.content})'