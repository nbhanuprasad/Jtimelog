from django.apps import AppConfig
import os
from django.conf import settings


class TimelogappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'timelogapp'
    path = './timelogapp'
