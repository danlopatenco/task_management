from pathlib import Path
from datetime import timedelta
from .utils import (
    get_env_var,
    get_int_env_var
)


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-m$w2bj58&#gathbl5k4+!#7+xck&@mrr$rfzwn^mulp-8di4k*'

DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    "drf_yasg",
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    'djoser',
    'corsheaders',
    'core',
    'projects',
    'tasks',
    'time_tracking',
    'app_messages'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'management_tool.urls'

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

WSGI_APPLICATION = 'management_tool.wsgi.application'


POSTGRES_HOST = get_env_var("POSTGRES_HOST")
POSTGRES_PORT = get_int_env_var("POSTGRES_PORT", 5432)
POSTGRES_DB = get_env_var("POSTGRES_DB")
POSTGRES_USER = get_env_var("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_var("POSTGRES_PASSWORD")


DATABASES = {
    'default': {
        "ENGINE": 'django.db.backends.postgresql',
        "HOST": POSTGRES_HOST,
        "NAME": POSTGRES_DB,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD
    }
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


SIMPLE_JWT = {
    # "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# # DJOSER CONFIG
# DJOSER = {
#     "LOGIN_FIELD": "email",
#     "USER_CREATE_PASSWORD_RETYPE": True,
#     "USERNAME_CHANGED_EMAIL_CONFIRMATION": True,
#     "PASSWORD_CHANGED_EMAIL_CONFIRMATION": True,
#     "SEND_CONFIRMATION_EMAIL": True,
#     "SET_USERNAME_RETYPE": True,
#     "SET_PASSWORD_RETYPE": True,
#     "USERNAME_RESET_CONFIRM_URL": "password/reset/confirm/{uid}/{token}",
#     "PASSWORD_RESET_CONFIRM_URL": "email/reset/confirm/{uid}/{token}",
#     "ACTIVATION_URL": "activate/{uid}/{token}",
#     "SEND_ACTIVATION_EMAIL": True,
#     "SOCIAL_AUTH_TOKEN_STRATEGY": "djoser.social.token.jwt.TokenStrategy",
#     "SOCIAL_AUTH_ALLOWED_REDIRECT_URIS": [
#         "your redirect url",
#         "your redirect url",
#     ],
#     "SERIALIZERS": {
#         "user_create": "accounts.serializers.UserCreateSerializer",  # custom serializer
#         "user": "djoser.serializers.UserSerializer",
#         "current_user": "djoser.serializers.UserSerializer",
#         "user_delete": "djoser.serializers.UserSerializer",
#     },
# }

# CORS HEADERS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
