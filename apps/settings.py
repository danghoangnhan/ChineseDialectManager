import os
from pathlib import Path
import urllib3
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = str(BASE_DIR) + '/envs/dev.env'
load_dotenv(dotenv_path=env_path)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ge356@&9l9=djmz073s&r7na@(bhf%r**tho)jt^din*sfs)1w'


# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'dictionary',
    'vocabulary',
    'rules',
    'django_admin_row_actions',
    'django_object_actions',
    'import_export',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "author.middlewares.AuthorDefaultBackendMiddleware",

]

ROOT_URLCONF = 'apps.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'apps.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        }
    }
}

BROKER_URL = os.environ.get("REDIS_URL", "redis://0.0.0.0:6379/0")
REDIS_URL = os.environ.get("REDIS_URL", "'redis://0.0.0.0:6379/0'")

STORAGES = {
    "IMPORT_EXPORT_CELERY_STORAGE": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
}


def getVocabularyResource():
    from vocabulary.resource import VocabularyResource
    return VocabularyResource


IMPORT_EXPORT_CELERY_MODELS = {
    "vocabulary": {
        "app_label": "vocabulary",
        "model_name": "vocabulary",
        'resource': getVocabularyResource
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Taipei'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = "/static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static'
]
DEBUG = True
urllib3.disable_warnings()

# IMPORT_EXPORT_USE_TRANSACTIONS = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
IMPORT_EXPORT_SKIP_ADMIN_CONFIRM = True
