import os

DIRNAME = os.path.dirname(__file__)

DEBUG = True

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = os.path.join(DIRNAME, 'treenav.db')

ROOT_URLCONF = 'treenav.tests.urls'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'mptt',
    'treenav',
    'treenav.tests',
)
