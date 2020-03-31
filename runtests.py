#!/usr/bin/env python
import sys

import django
from django.conf import settings
from django.test.utils import get_runner


if not settings.configured:
    settings.configure(
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:',
            }
        },
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'mptt',
            'treenav',
        ),
        MIDDLEWARE=(
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.common.CommonMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.template.context_processors.debug',
                        'django.template.context_processors.i18n',
                        'django.template.context_processors.media',
                        'django.template.context_processors.static',
                        'django.template.context_processors.tz',
                        'django.contrib.messages.context_processors.messages',
                        "django.template.context_processors.request",
                        "treenav.context_processors.treenav_active",
                    ],
                },
            },
        ],
        # Load models directly to pick up test-only models
        # See: http://stackoverflow.com/a/25267435/347942
        MIGRATION_MODULES={'treenav': None},
        SECRET_KEY='this-is-just-for-tests-so-not-that-secret',
        ROOT_URLCONF='treenav.tests.urls',
    )


def runtests():
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=1, interactive=True, failfast=False)
    failures = test_runner.run_tests(['treenav.tests.test_templatetags', ])
    sys.exit(failures)


if __name__ == '__main__':
    runtests()
