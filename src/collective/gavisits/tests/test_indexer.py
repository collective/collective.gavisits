# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.gavisits.testing import INTEGRATION_TESTING
from collective.gavisits.testing import overrideAdaptersAndUtilities


class TestValueIndexed(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('test_type', "test_content")
        self.context_behavior = self.portal['test_content']
        self.portal.invokeFactory('test_type_no_behavior', "test_content_no_behavior")
        self.context_no_behavior = self.portal['test_content_no_behavior']

    def test_object_provides_behavior_indexed(self):
        pc = self.portal.portal_catalog
        self.assertEquals(pc.uniqueValuesFor('visits'), (0,))
        overrideAdaptersAndUtilities(self.context_behavior)

        view = self.context_behavior.restrictedTraverse("@@update-visits-counter")
        view()
        
        self.assertEquals(pc.uniqueValuesFor('visits'), (200,))
        
        view = self.context_no_behavior.restrictedTraverse("@@update-visits-counter")
        view()

        self.assertEquals(pc.uniqueValuesFor('visits'), (200,))

    def test_invalid_read_no_override_old_value(self):
        pc = self.portal.portal_catalog
        
        self.context_behavior.visits = 120
        self.context_behavior.reindexObject(idxs=['visits',])
        
        self.assertEquals(pc.uniqueValuesFor('visits'), (120,))
        
        view = self.context_behavior.restrictedTraverse("@@update-visits-counter")
        view()

        self.assertEquals(pc.uniqueValuesFor('visits'), (120,))
        
        overrideAdaptersAndUtilities(self.context_behavior)

        view = self.context_behavior.restrictedTraverse("@@update-visits-counter")
        view()

        self.assertEquals(pc.uniqueValuesFor('visits'), (200,))
        
    def test_do_not_index_AT(self):
        pc = self.portal.portal_catalog
        self.assertEquals(pc.uniqueValuesFor('visits'), (0,))
        self.portal.invokeFactory('Document', "document")
        document = self.portal['document']
        document.reindexObject(idxs=['visits',])
