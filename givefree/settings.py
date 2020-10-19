import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config('SECRET_KEY', default='very-secret-key')
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['*', 'localhost', '34.121.77.125']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
    'bootstrap4',
    'mptt',
    'easy_thumbnails',
    'meta',

    'users.apps.UsersConfig',
    'freestuff.apps.FreestuffConfig',
    'cart.apps.CartConfig',
    'orders.apps.OrdersConfig',
    'coupons.apps.CouponsConfig',
    'pages.apps.PagesConfig',
]

META_DEFAULT_KEYWORDS = ['віддам безкоштовно', 'поторгуємось', 'гаражна розпродаж',
                         'товар', 'річ', 'купити', 'дешево', 'безкоштовно',
                         ]

META_INCLUDE_KEYWORDS = ['віддам безкоштовно', 'поторгуємось', 'гаражна розпродаж',
                         'товар', 'річ', 'купити', 'дешево', 'безкоштовно',
                         ]

THUMBNAIL_ALIASES = {
    '': {
        'mini': {'size': (100, 100), 'crop': True},
        'avatar': {'size': (200, 200), 'crop': True},
        'small': {'size': (300, 300), 'crop': True},
        'large': {'size': (800, 800), 'crop': True},
    },
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'givefree.urls'

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
                'cart.context_processors.cart',
                'cart.context_processors.cart_pk',
            ],
        },
    },
]

WSGI_APPLICATION = 'givefree.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': config('DATABASE_ENGINE', default='django.db.backends.sqlite3'),
        'NAME': config('DATABASE_NAME', default='db.sqlite3'),
        'USER': config('DATABASE_USER', default=None),
        'PASSWORD': config('DATABASE_PASSWORD', default=None),
        'HOST': config('DATABASE_HOST', default=None),
        'PORT': config('DATABASE_PORT', cast=int, default=0),
    }
}

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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

AUTH_USER_MODEL = 'users.CustomUser'

AUTHENTICATION_BACKENDS = {
    # 'django.contrib.auth.backends.ModelBackend',
    'users.authenticate.CustomModelBackend',
    # 'social_core.backends.facebook.FacebookOAuth2',
    # 'social_core.backends.google.GoogleOAuth2',
}

LANGUAGE_CODE = 'uk'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'givefree/static/'),]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

CART_SESSION_ID = 'cart'

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'users:profile'
LOGOUT_REDIRECT_URL = "freestuff:things_list"
PASSWORD_RESET_TIMEOUT_DAYS = 1

SITE_ID = 1

CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_ENABLE_UTC = True
CELERY_BROKER_URL = 'amqp://guest@localhost:5672//'

OLD_PASSWORD_FIELD_ENABLED = True
LOGOUT_ON_PASSWORD_CHANGE = False

LOGGING_CONFIG = 'logging.config.dictConfig'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': os.path.join(BASE_DIR, 'logs/django/debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO',
        },
    }
}

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default=None)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default=None)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default=None)
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=0)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=False)
SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1