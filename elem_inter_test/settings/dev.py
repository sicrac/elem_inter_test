from base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'NAME': 'dev',
        'PORT': '5432'
    }
}


INSTALLED_APPS = [
    'image_data.apps.ImageDataConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MEDIA_ROOT = 'media'

# Custom settings

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

CSV_URL = "https://docs.google.com/spreadsheet/ccc?key=0Aqg9JQbnOwBwdEZFN2JKeldGZGFzUWVrNDBsczZxLUE&single=true&gid=0&output=csv"

IMAGE_SIZE = 120, 120
