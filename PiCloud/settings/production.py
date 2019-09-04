"""
Django settings for PiCloud project production environment.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

from .common import *

SECRET_KEY = get_config('SECRET_KEY')

DEBUG = False

DATABASES = {
    'default': get_config('DEFAULT_DATABASE')
}
