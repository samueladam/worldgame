import os.path

DEBUG = True

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

GDAL_LIBRARY_PATH = os.path.join(PROJECT_PATH, '../../parts/libgdal/lib/libgdal.so')
GEOS_LIBRARY_PATH = os.path.join(PROJECT_PATH, '../../parts/libgeos/lib/libgeos_c.so')


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'worldgame',
        'USER': 'worldgame',
        'PASSWORD': 'worldgame',

    }
}

MEDIA_ROOT = os.path.join(PROJECT_PATH, 'static/')
MEDIA_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

TEMPLATE_DIRS = (
   PROJECT_PATH,
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django.contrib.gis',
    'django_extensions',
    'worldgame',
)

ROOT_URLCONF = 'worldgame.urls'
