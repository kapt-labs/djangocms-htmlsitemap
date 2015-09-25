# -*- coding: utf-8 -*-

# Standard library imports
import os

# Third party imports
from django import VERSION as DJANGO_VERSION
from django.conf import global_settings as default_settings

# Local application / specific library imports


TEST_ROOT = os.path.abspath(os.path.dirname(__file__))

# Helper function to extract absolute path
location = lambda x: os.path.join(TEST_ROOT, x)


class DisableMigrations(object):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return 'notmigrations'


DEBUG = False
TEMPLATE_DEBUG = False

SECRET_KEY = 'key'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    },
}

if DJANGO_VERSION >= (1, 8):
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': (
                location('_testsite/templates'),
            ),
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.request',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                    'cms.context_processors.cms_settings',
                    'sekizai.context_processors.sekizai',
                ],
            },
        },
    ]
else:
    TEMPLATE_CONTEXT_PROCESSORS = default_settings.TEMPLATE_CONTEXT_PROCESSORS + (
        'django.core.context_processors.request',
        'cms.context_processors.cms_settings',
    )
    TEMPLATE_DIRS = (
        location('_testsite/templates'),
    )

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sessions',
    'django.contrib.sites',

    'cms',
    'treebeard',
    'menus',
    'sekizai',
    'djangocms_admin_style',

    'djangocms_htmlsitemap',
    'tests',
] + ['django.contrib.admin', ]

MIGRATION_MODULES = DisableMigrations()
TEST_RUNNER = 'django.test.runner.DiscoverRunner'  # Hide checks

CMS_TEMPLATES = (
    ('index.html', 'Index'),
    ('simple.html', 'Simple'),
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

MEDIA_ROOT = '/media/'
STATIC_URL = '/static/'

USE_TZ = True
LANGUAGE_CODE = 'fr'
LANGUAGES = (
    ('fr', 'Français'),
    ('en', 'English'),
)

SITE_ID = 1

ROOT_URLCONF = 'tests._testsite.urls'

# Setting this explicitly prevents Django 1.7+ from showing a
# warning regarding a changed default test runner. The test
# suite is run with py.test, so it does not matter.
SILENCED_SYSTEM_CHECKS = ['1_6.W001']
