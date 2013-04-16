# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.gavisits.behavior import IVisitsCounter

from collective.gavisits.testing import INTEGRATION_TESTING
from collective.gavisits.testing import overrideAdaptersAndUtilities


class TestValueIndexed(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('test_type', "test_content")
        self.context = self.portal['test_content']

    def test_no_value_set_zero(self):
        behavior = IVisitsCounter(self.context)
        behavior._set_visits(None)
        self.assertEquals(self.context.visits,0)
        
    def test_no_int_raises(self):
        behavior = IVisitsCounter(self.context)
        self.assertRaises(ValueError, behavior._set_visits, "value")
