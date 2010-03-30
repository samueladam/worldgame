import os.path

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
    }
}

TEMPLATE_DIRS = (
   os.path.dirname(os.path.abspath(__file__)),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.messages',
    'django_extensions',
    'worldgame',
)

ROOT_URLCONF = 'worldgame.urls'
