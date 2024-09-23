from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['192.168.100.60']

#required apps
INSTALLED_APPS = [
    'daphne',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'apis',
    'rest_framework',
    'corsheaders',
    "django_mongoengine",
    'channels',
]

#cors for frontend
CORS_ALLOWED_ORIGINS = [
    'http://192.168.100.60:3000'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'wfmbackend.urls'

#WSGI_APPLICATION = 'wfmbackend.wsgi.application'

ASGI_APPLICATION = 'wfmbackend.asgi.application'

MONGODB_DATABASES = {
    'default': {
        'name': 'Remoteconnect',
        'host': 'localhost',
        'port': 27017,
        "tz_aware": True,
    },
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('localhost', 6379)],
        },
    },
}


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

SESSION_ENGINE = 'django_mongoengine.sessions'
SESSION_SERIALIZER = 'django_mongoengine.sessions.BSONSerializer'

SQUARE_APPLICATION_ID = os.getenv('SQUARE_APPLICATION_ID')
SQUARE_ACCESS_TOKEN = os.getenv('SQUARE_ACCESS_TOKEN')
SQUARE_ENVIRONMENT = os.getenv('SQUARE_ENVIRONMENT', default='sandbox')

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
