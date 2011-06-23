#!/usr/bin/env python
# Copyright (C) 2010 Linaro Limited
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

from setuptools import setup


setup(
    name='django-testproject',
    version=":versiontools:django_testproject:__version__",
    author="Zygmunt Krynicki",
    author_email="zygmunt.krynicki@linaro.org",
    description="Universal project for running unit tests of Django applications",
    url='https://launchpad.net/django-testproject',
    license='LGPLv3',
    keywords=['django', 'testing'],
    classifiers=[
        "Development Status :: 4 - Beta",
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Testing",
    ],
    zip_safe=True,
    packages=[
        'django_testproject',
    ],
    install_requires=[
        'django >= 1.0',
    ],
    setup_requires = [
        'versiontools >= 1.3.1',
    ],
    include_package_data=True,
)
