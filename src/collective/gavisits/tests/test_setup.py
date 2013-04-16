# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.gavisits.config import PROJECTNAME
from collective.gavisits.testing import INTEGRATION_TESTING


class InstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_installed(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled(PROJECTNAME))


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_uninstalled(self):
        qi = getattr(self.portal, 'portal_quickinstaller')
        qi.uninstallProducts(products=[PROJECTNAME])
        self.assertFalse(qi.isProductInstalled(PROJECTNAME))
