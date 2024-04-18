from pathlib import Path
from decouple import config
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG')

ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework_simplejwt.token_blacklist',
    'django_rest_passwordreset',
    'rest_framework_simplejwt',
    'rest_framework',
    'student',
]


# middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'options': '-c search_path=django,public'
        },
        'NAME': config('PGDB_NAME'), # type: ignore # noqa 
        'USER': config('PGDB_USER'), # type: ignore # noqa
        'PASSWORD': config('PGDB_PASSWORD'), # type: ignore # noqa
        'HOST': config('PGDB_HOST'), # type: ignore # noqa
        'port': config('PGDB_PORT') # type: ignore # noqa
    }
}


# Password validation
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

AUTH_USER_MODEL = 'student.Student'

# Internationalization
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# ---------------- Rest framework config ---------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# ----------------- redis connection ---------------
CACHES_TTL = config('CACHES_TTL')# type: ignore # noqa

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": config('RD_LOCATION'), # type: ignore # noqa
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient", # type: ignore # noqa
            "PASSWORD": config('RD_PASSWORD') # type: ignore # noqa
        }
    }
}

# ----------------- Email configuration -------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST') # type: ignore # noqa
EMAIL_USE_TLS = config('EMAIL_USE_TLS') # type: ignore # noqa
EMAIL_PORT = config('EMAIL_PORT') # type: ignore # noqa
EMAIL_HOST_USER = config('EMAIL_HOST_USER') # type: ignore # noqa
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD') # type: ignore # noqa

# --------------------- JWT CONFIG --------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(config('ACCESS_TOKEN_LIFETIME_IN_MINUTE'))), # type: ignore # noqa
    'REFRESH_TOKEN_LIFETIME': timedelta(minutes=int(config('REFRESH_TOKEN_LIFETIME_IN_MINUTE'))), # type: ignore # noqa
    "ROTATE_REFRESH_TOKENS": True,
    "UPDATE_LAST_LOGIN": True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'SIGNING_KEY': config('SECRET_KEY'), # type: ignore # noqa
    'VERIFYING_KEY': config('SECRET_KEY'), # type: ignore # noqa
    'ALGORITHM': 'HS256',
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'

# media settings
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# logging
# DEBUG_LOGGING = config('DEBUG_LOGGING', 'OFF') # type: ignore # noqa

# LOGGING = {
#     'version': 1,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             # 'filters': ['require_debug_true'],
#             'filters': ['require_debug_true'] if DEBUG_LOGGING.upper() == 'ON' else [],
#             'class': 'logging.StreamHandler',
#         }
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'] if DEBUG_LOGGING.upper() == 'ON' else [],
#         }
#     }
# }
