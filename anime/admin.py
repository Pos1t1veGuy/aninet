from django.contrib import admin
from .models import Anime, Season, Episode, Dub, Comment

@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ['rus_name', 'slug', 'views']

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    list_display = ['anime', 'number', 'release_date', 'released']

@admin.register(Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ['rus_name', 'season', 'number', 'views']

@admin.register(Dub)
class DubAdmin(admin.ModelAdmin):
    list_display = ['author', 'episode', 'views']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'episode', 'date_sent', 'content']
