from django.apps import AppConfig
from django.conf import settings

from shutil import rmtree

import os


class AuthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AUTH'