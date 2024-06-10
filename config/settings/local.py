import mongoengine
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_EXPOSE_HEADERS = ['Content-Disposition']

CSRF_TRUSTED_ORIGINS = []

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

MONGO_USER = os.getenv('MONGO_USER') if os.getenv('MONGO_USER') else ''
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD') if os.getenv('MONGO_PASSWORD') else ''
MONGO_HOST = os.getenv('MONGO_HOST') if os.getenv('MONGO_HOST') else ''
MONGO_PORT = os.getenv('MONGO_PORT') if os.getenv('MONGO_PORT') else ''
MONGO_DB = os.getenv('MONGO_DB') if os.getenv('MONGO_DB') else ''

mongoengine.connect(db=MONGO_DB, host=MONGO_HOST, username=MONGO_USER, password=MONGO_PASSWORD, port=int(MONGO_PORT), uuidRepresentation='standard')