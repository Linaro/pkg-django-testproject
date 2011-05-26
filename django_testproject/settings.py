# Copyright (C) 2010, 2011 Linaro Limited
#
# Author: Zygmunt Krynicki <zygmunt.krynicki@linaro.org>
#
# This file is part of django-testproject.
#
# django-testproject is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation
#
# django-testproject is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with django-testproject.  If not, see <http://www.gnu.org/licenses/>.

"""
Settings generator for test projects
"""

import inspect
import os
import sys

import django


DJANGO_TESTPROJECT_DIR = os.path.abspath(os.path.dirname(__file__))


def _get_default_settings(project_dir):
    """
    Produce default settings
    """
    SECRET_KEY = ''
    TIME_ZONE = 'Europe/Warsaw'
    ADMINS = (
        #( 'Your name', 'email@example.org'),
        )
    MEDIA_ROOT = ''
    MEDIA_URL = ''
    ADMIN_MEDIA_PREFIX = '/media/'
    LANGUAGE_CODE = 'en-us'
    USE_I18N = True
    DEBUG = True
    TEMPLATE_DEBUG = False
    MANAGERS = ADMINS
    ROOT_URLCONF = ''
    SITE_ID = 1
    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.load_template_source',
        'django.template.loaders.app_directories.load_template_source',)
    TEMPLATE_DIRS = (
        os.path.join(project_dir, "templates"),
        os.path.join(DJANGO_TESTPROJECT_DIR, "templates"))
    TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.i18n",
        "django.core.context_processors.media",
        "django.contrib.messages.context_processors.messages")
    MIDDLEWARE_CLASSES = (
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.middleware.transaction.TransactionMiddleware',)
    if django.VERSION[0:2] >= (1, 2):
        DATABASES = {
            'default': {
                # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
                'ENGINE': 'django.db.backends.sqlite3',
                # Or path to database file if using sqlite3.
                'NAME': os.path.join(project_dir, 'test.db'),
                'USER': '',  # Not used with sqlite3.
                'PASSWORD': '',  # Not used with sqlite3.
                'HOST': '',  # Set to empty string for localhost. Not used with sqlite3.
                'PORT': '',  # Set to empty string for default. Not used with sqlite3.
            }}
    else:
        DATABASE_ENGINE = 'sqlite3'
        DATABASE_NAME = os.path.join(project_dir, 'test.db')
        DATABASE_USER = ''
        DATABASE_PASSWORD = ''
        DATABASE_HOST = ''
        DATABASE_PORT = ''
    return locals()


def gen_settings(**kwargs):
    """
    Generate settings for test project

    The settings will work for django 1.1.x and 1.2.x

    You may provide any additional settings with keyword arguments, they
    will be merged with generated settings.
    """
    # Find project_dir by inspecting caller
    frame = inspect.currentframe()
    outer_frames = inspect.getouterframes(frame)
    caller = outer_frames[1][0]
    project_dir = os.path.dirname(
        os.path.abspath(
            inspect.getsourcefile(caller)))

    # Default settings
    settings = _get_default_settings(project_dir)

    # Merge with user provided defaults
    for key, value in kwargs.iteritems():
        if key not in settings:
            new_value = value
        elif isinstance(settings[key], (list, tuple)) and isinstance(value, (list, tuple)):
            # Merge lists
            new_value = list(settings[key]) + list(value)
        elif isinstance(settings[key], (int, float, bool, basestring)) and isinstance(value, (int, float, bool, basestring)):
            # Overwrite simple types
            new_value = value
        else:
            raise ValueError("Don't know how to merge custom setting %r that already exists in generated settings" % key)
        settings[key] = new_value

    # Crude django_coverage integration
    try:
        import django_coverage
        settings['INSTALLED_APPS'].insert(0, 'django_coverage')
        settings['COVERAGE_REPORT_HTML_OUTPUT_DIR'] = os.getenv("COVERAGE_REPORT_HTML_OUTPUT_DIR")
        settings['COVERAGE_MODULE_EXCLUDES'] = []
    except ImportError:
        pass

    # Return settings back to the caller
    return settings
