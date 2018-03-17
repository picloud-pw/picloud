"""
Django settings for PiCloud project development.
"""

# Development settings are unsuitable for production.
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

from .common import *

import random

# In development environment, we generate a random SECRET_KEY at each server startup
SECRET_KEY = ''.join([
    random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)')
    for i in range(50)
])

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
