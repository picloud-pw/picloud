import json
import os
from json import JSONDecodeError

from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SECRETS_FILE_VAR = 'APPLICATION_SECRETS'

if SECRETS_FILE_VAR in os.environ:
    with open(os.environ.get(SECRETS_FILE_VAR)) as f:
        json_config = None
        try:
            json_config = json.loads(f.read())
        except JSONDecodeError as e:
            error_msg = "{} is an invalid JSON file: {} (error at line {}, col {})" \
                .format(SECRETS_FILE_VAR, e.msg, e.lineno, e.colno)
            raise ImproperlyConfigured(error_msg)
else:
    raise ImproperlyConfigured("{} environment variable is not set".format(SECRETS_FILE_VAR))


def get_config(setting, config=json_config):
    try:
        val = config[setting]
        if val == 'True':
            val = True
        elif val == 'False':
            val = False
        return val
    except KeyError:
        error_msg = "Configuration variable {0} not found in settings map".format(setting)
        raise ImproperlyConfigured(error_msg)


# Application definition

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloud',
    'django.contrib.admin',
    'django.contrib.auth',
]

ROOT_URLCONF = 'PiCloud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

WSGI_APPLICATION = 'PiCloud.wsgi.application'

EMAIL_USE_TLS = True
EMAIL_HOST = get_config('EMAIL_HOST')
EMAIL_HOST_USER = get_config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = get_config('EMAIL_PORT')

GOOGLE_RECAPTCHA_SECRET_KEY = get_config('GOOGLE_RECAPTCHA_SECRET_KEY')
