import os
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_EXPOSE_HEADERS = ['Content-Disposition']

CSRF_TRUSTED_ORIGINS = []


MIDDLEWARE += ['whitenoise.middleware.WhiteNoiseMiddleware']

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB') if os.getenv('POSTGRES_DB') else '',
        'USER': os.getenv('POSTGRES_USER') if os.getenv('POSTGRES_USER') else '',
        'PASSWORD': os.getenv('POSTGRES_PASSWORD') if os.getenv('POSTGRES_PASSWORD') else '',
        'HOST': os.getenv('POSTGRES_HOST') if os.getenv('POSTGRES_HOST') else '',
        'PORT': os.getenv('POSTGRES_PORT') if os.getenv('POSTGRES_PORT') else ''
    }
}