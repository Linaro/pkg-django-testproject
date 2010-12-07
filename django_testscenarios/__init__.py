# Copyright (C) 2010 Linaro Limited
#
# Author: Zygmunt Krynicki <zygmunt.krynicki@linaro.org>
#
# This file is part of django-testscenarios.
#
# django-testscenarios is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation
#
# django-testscenarios is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with django-testscenarios.  If not, see <http://www.gnu.org/licenses/>.

"""
An uber-test class for Django that mixes:
 * testtools.TestCase
 * testscenarios.TestWithScenarios
with django.test.TestCase or TransactionTestCase

This module contains two base classes for django aware unit testing with
scenario support. They change the way __call__ and run() are implemented
to let each test case generated for a scenario participate in django
database setup mechanics.
"""

import django.test
import testscenarios
import testtools
import unittest


class ScenarioAwareTestCaseIdStrReprMixIn(object):
    """
    Helper mix-in that makes the id(), str() and repr() methods sensible
    again. It uses code from unittest.TestCase as starting point and
    adds the scenario name where appropriate.

    It's needed to undo the changes that testtools and testscenarios
    make which somewhat collide with django test runner. The code has
    been tuned to make output match normal django test code.
    """

    _testScenarioName = None

    def id(self):
        value = unittest.TestCase.id(self)
        if self._testScenarioName is not None:
            value += ' (%s)' % self._testScenarioName
        return value

    def __str__(self):
        value = unittest.TestCase.__str__(self)
        if self._testScenarioName is not None:
            value += ' (%s)' % self._testScenarioName
        return value

    def __repr__(self):
        if self._testScenarioName is not None:
            return unittest.TestCase.__repr__(self)
        else:
            return "<%s.%s testMethod=%s testScenario=%s>" % (
                self.__class__.__module__,
                self.__class__.__name__,
                self._testMethodName,
                self._testScenarioName
            )

    def shortDescription(self):
        # XXX this makes setup.py test and test_project/manage.py test
        # output consistent but I have not managed to understand why
        # it's needed. Perhaps something along the way sets
        # shortDescription() in the non-pure-unittest code path and then
        # it gets used by TextTestRunner's getDescription() method.
        return str(self)


class TestCase(
    ScenarioAwareTestCaseIdStrReprMixIn,
    testtools.TestCase,
    django.test.TestCase):
    """
    Django TestCase with testtools power.
    """


class TransactionTestCase(
    ScenarioAwareTestCaseIdStrReprMixIn,
    testtools.TestCase,
    django.test.TransactionTestCase):
    """
    Django TransactionTestCase with testtools power.
    """


class TestCaseWithScenarios(
    ScenarioAwareTestCaseIdStrReprMixIn,
    testtools.TestCase,
    testscenarios.TestWithScenarios,
    django.test.TestCase):
    """
    Django TestCase with testtools power and scenario support.
    """

    def __call__(self, result=None):
        """
        Wrapper around default __call__ method to perform common Django test
        set up. This means that user-defined Test Cases aren't required to
        include a call to super().setUp().

        This wrapper is made scenario-aware
        """
        scenarios = self._get_scenarios()
        if scenarios:
            # Note, we call our implementation of run() to create
            # scenarios and give each a chance to initialize.
            self.run(result)
        else:
            # Without scenarios we just call the django __call__ version
            # to let it initialize the test database
            return django.test.TransactionTestCase.__call__(self, result)

    def run(self, result=None):
        """
        Run test case generating additional scenarios if needed
        """
        scenarios = self._get_scenarios()
        if scenarios:
            # We can get the scenario name like that because
            # generate_scenarios iterates the list of scenarios in order
            for scenario_info, test in zip(scenarios,
                                           testscenarios.scenarios.generate_scenarios(self)):
                # Monkey-patch id() back into the cloned test class
                # This will use our id (which resembles stock TestCase.id()
                # but it will hold extra information about test scenario
                # that was applied. This is necessary because
                # testscenarios removes any information about the actual
                # scenario and hard-codes the id() function to return
                # something that we cannot control.
                test._testScenarioName = scenario_info[0]
                test.id = lambda: self.__class__.id(test)

                # Note, we call __call__ on the test case instance to
                # give django's TestCase __call__ a chance to run.  The
                # code there will actually setup all the database
                # mechanics. If we would simply call run here it'd loop
                # back to our implementation instead which would go to
                # the else caluse and call django's TestCase.run(). The
                # problem with this code is that it depends on __call__
                # being called earlier. This normally happens when the
                # test framework calls into the test (the very first
                # call to a unittest.TestCase subclass is __call__, not
                # __run__.
                test.__call__(result)
            return
        else:
            return super(TestCaseWithScenarios, self).run(result)


class TransactionTestCaseWithScenarios(TestCaseWithScenarios):
    """
    Django TransactionTestCase with testtools power and scenario support.
    """

    def _fixture_setup(self):
        # We have to call the proper implementation directly since
        # django.test.TestCase (without scenarios) _also_ has this
        # method and comes earlier in the inheritance chain's method
        # resolution order.
        django.test.TransactionTestCase._fixture_setup(self)

    def _fixture_teardown(self):
        # We have to call the proper implementation directly since
        # django.test.TestCase (without scenarios) _also_ has this
        # method and comes earlier in the inheritance chain's method
        # resolution order.
        django.test.TransactionTestCase._fixture_teardown(self)


__all__ = [
    "TestCase",
    "TestCaseWithScenarios",
    "TransactionTestCase",
    "TransactionTestCaseWithScenarios"
]
