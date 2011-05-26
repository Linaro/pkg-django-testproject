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
Helper function for running tests via setup.py test
"""

import os
import sys

import django


def run_tests_for(settings_module_name, test_last_n_apps=-1):
    """
    Helper function that simplifies testing Django applications via setup.py
    test

    The idea is to test your application in a small test project. Since not
    everything in your project is relevant (you don't want to test
    django.contrib.auth gazillion times just because you use it in your
    application) run_tests allows you to run just a subset of applications. By
    default last item in INSTALLED_APPLICATIONS is tested. You can change it by
    calling run_tests() with different argument. If you really want to test all
    applications just pass None as test_last_n_apps.
    """
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module_name

    from django.conf import settings
    from django.test.utils import get_runner
    if test_last_n_apps is None:
        test_labels = None
    else:
        test_labels = settings.INSTALLED_APPS[test_last_n_apps:]
    if django.VERSION[0:2] <= (1, 1):
        # Prior to django 1.2 the runner was a plain function
        runner_fn = get_runner(settings)
        runner = lambda test_labels: runner_fn(test_labels, verbosity=2, interactive=False)
    else:
        # After 1.2 the runner is a class
        runner_cls = get_runner(settings)
        runner = runner_cls(verbosity=2, interactive=False).run_tests
    failures = runner(test_labels)
    sys.exit(failures)


def run_tests(test_last_n_apps=-1):
    """
    Like run_tests_for but assumes that settings_module_name is
    "test_project.settings"
    """
    return run_tests_for("test_project.settings", test_last_n_apps)
