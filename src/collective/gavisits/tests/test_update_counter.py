# -*- coding: utf-8 -*-

import unittest2 as unittest

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from collective.gavisits.testing import INTEGRATION_TESTING
from collective.gavisits.testing import overrideAdaptersAndUtilities


class TestUpdateVisitsCounterView(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('test_type', "test_content")
        self.context = self.portal['test_content']

    def test_get_visits_no_ga_account(self):
        view = self.context.restrictedTraverse("@@update-visits-counter")
        self.assertIsNone(view.get_visits())

    def test_get_visits_valid_ga_account(self):
        overrideAdaptersAndUtilities(self.context)
        view = self.context.restrictedTraverse("@@update-visits-counter")
        self.assertEquals(view.get_visits(), 200)

    def test_headers(self):      
        view = self.context.restrictedTraverse("@@update-visits-counter")
        view()
        cc = self.layer['request'].response.getHeader('Cache-Control')
        ct = self.layer['request'].response.getHeader('Content-Type')
        self.assertEquals(cc, 'max-age=120, s-maxage=120,public')
        self.assertEquals(ct, 'application/json;charset=utf-8')

    def test_view_results_no_data(self):
        view = self.context.restrictedTraverse("@@update-visits-counter")
        results = view()
        self.assertEquals(results, '{"visits": -1}')

    def test_view_results_valid_data(self):
        overrideAdaptersAndUtilities(self.context)
        view = self.context.restrictedTraverse("@@update-visits-counter")
        results = view()
        self.assertEquals(results, '{"visits": 200}')

    def test_provide_both_dates_to_override(self):
        overrideAdaptersAndUtilities(self.context)
        analytics_tool = self.context.portal_analytics

        request = self.layer['request']

        view = self.context.restrictedTraverse("@@update-visits-counter")
        view()
        
        start_date = request.get('start_date')
        end_date = request.get('end_date')
        
        date = self.context.created().strftime('%Y%m%d')
        
        self.assertEquals(start_date, date)
        self.assertEquals(end_date, date)
        
        report = analytics_tool['collective-gavisits-visits']
        report.start_date = '20010101'
        view()
        
        start_date = request.get('start_date')
        end_date = request.get('end_date')
        
        self.assertEquals(start_date, date)
        self.assertNotEquals(start_date, '20010101')
        self.assertEquals(end_date, date)
        
        report.end_date = '20010101'
        view()
        
        start_date = request.get('start_date')
        end_date = request.get('end_date')
        
        self.assertNotEquals(start_date, date)
        self.assertEquals(start_date, '20010101')
        self.assertNotEquals(end_date, date)
        self.assertEquals(end_date, '20010101')
