import json
import os
from json import JSONDecodeError
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent


def get_config(setting):
    try:
        val = os.environ.get(setting)
        if val == 'True':
            val = True
        elif val == 'False':
            val = False
        elif ((val.startswith("[") and val.endswith("]")) or
              (val.startswith("{") and val.endswith("}"))):
            try:
                val = json.loads(val)
            except JSONDecodeError:
                pass
        return val
    except KeyError:
        error_msg = "Configuration variable {0} not found in settings map".format(setting)
        raise ImproperlyConfigured(error_msg)


# Application definition

ALLOWED_HOSTS = get_config('ALLOWED_HOSTS')
CSRF_TRUSTED_ORIGINS = get_config("CSRF_TRUSTED_ORIGINS")

SECURE_SSL_REDIRECT = get_config("SECURE_SSL_REDIRECT")
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
SECURE_REDIRECT_EXEMPT = [
    r'^health$',
]

SECRET_KEY = get_config('SECRET_KEY')

DEBUG = get_config('DEBUG')

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.environ.get("POSTGRESQL_NAME"),
        "USER": os.environ.get("POSTGRESQL_USER"),
        "PASSWORD": os.environ.get("POSTGRESQL_PASSWORD"),
        "HOST": os.environ.get("POSTGRESQL_HOST"),
        "PORT": os.environ.get("POSTGRESQL_PORT"),
    }
}

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.auth',

    'social_django',

    'cloud',
    'website',
    'chats',
    'hierarchy',
    'posts',
    'memes',
    'students',
    'search',
]

ROOT_URLCONF = 'picloud.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# django-social-auth settings

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.github.GithubOAuth2',
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
SOCIAL_AUTH_REDIRECT_IS_HTTPS = get_config("SOCIAL_AUTH_REDIRECT_IS_HTTPS")

SOCIAL_AUTH_URL_NAMESPACE = 'social'

LOGIN_URL = '/auth/login/google-oauth2/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = get_config("SOCIAL_AUTH_GOOGLE_OAUTH2_KEY")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = get_config("SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_VK_OAUTH2_KEY = get_config("SOCIAL_AUTH_VK_OAUTH2_KEY")
SOCIAL_AUTH_VK_OAUTH2_SECRET = get_config("SOCIAL_AUTH_VK_OAUTH2_SECRET")
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_GITHUB_KEY = get_config("SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = get_config("SOCIAL_AUTH_GITHUB_SECRET")

SOCIAL_AUTH_LOGIN_REDIRECT_URL = "/after_login"

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
STATIC_ROOT = os.path.join(os.environ.get("STATIC_ROOT"))

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.environ.get("MEDIA_ROOT"))

WSGI_APPLICATION = 'picloud.wsgi.application'

EMAIL_USE_TLS = True
EMAIL_HOST = get_config('EMAIL_HOST')
EMAIL_HOST_USER = get_config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = get_config('EMAIL_PORT')

VK_GLOBAL_TOKEN = get_config('VK_GLOBAL_TOKEN')
VK_GROUP_TOKEN = get_config('VK_GROUP_TOKEN')
VK_API_VERSION = '5.131'

# FIXME XXX HACK: Подвергает сайт риску XSS, хотя и позволяет аутентифицироваться через REST
SESSION_COOKIE_HTTPONLY = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
