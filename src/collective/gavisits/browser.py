
import json
import logging

from datetime import date

from zope.component import getMultiAdapter
from zope.component import getUtility

from zope.interface import implements
from zope.interface import Interface

from zope.schema.interfaces import IVocabularyFactory

from Products.CMFCore.utils import getToolByName

from Products.Five.browser import BrowserView

from collective.googleanalytics.interfaces.plugins import IAnalyticsPlugin, \
    IAnalyticsDateRangeChoices
from collective.googleanalytics.interfaces.report import IAnalyticsReportRenderer

from collective.gavisits.behavior import IVisitsCounter

logger = logging.getLogger('collective.gavisits')


class UpdateVisitsCounter(BrowserView):

    def __call__(self):
        visits = self.get_visits()

        if visits:
            # Update object's value and reindex
            try:
                behavior = IVisitsCounter(self.context)
            except TypeError:
                behavior = None

            if behavior:
                behavior.visits = visits
                self.context.reindexObject(idxs=['visits',])

        else:
            visits = -1

        data = {'visits': visits}
        self.headers()

        return json.dumps(data, encoding='utf-8', ensure_ascii=False)

    def headers(self):
        self.request.response.setHeader('Content-Type',
                                        'application/json;charset=utf-8')
        # Two minutes cache both in browser and in proxy so we avoid hitting
        # 
        self.request.response.setHeader('Cache-Control',
                                        'max-age=120, s-maxage=120,public')

    def get_visits(self):
        result = None
        analytics_tool = getToolByName(self.context, 'portal_analytics', None)
        report = analytics_tool['collective-gavisits-visits']
        profile_ids = analytics_tool.reports_profile

        if profile_ids:
            self.request.set('profile_ids', profile_ids)
            
            if not (report.start_date and report.end_date):
                choices_provider = getMultiAdapter(
                    (self.context, self.request, report), IAnalyticsDateRangeChoices
                )

                choices = choices_provider.getChoices()
                
                if 'published' in choices:
                    dates = choices['published']
                else:
                    dates = choices['year']

            else:
                dates = [report.start_date, report.end_date]
        
            start_date = dates[0].strftime('%Y%m%d') if\
                            isinstance(dates[0], date) else dates[0]
            end_date = dates[1].strftime('%Y%m%d') if\
                            isinstance(dates[1], date) else dates[1]

            self.request.set('start_date', start_date)
            self.request.set('end_date', end_date)
            
            portal_state = getMultiAdapter((self.context, self.request), 
                                            name=u'plone_portal_state')
            site = portal_state.portal()
            site_path = site.getPhysicalPath()

            context_path = self.context.getPhysicalPath()

            relative_path = context_path[len(site_path):]

            path = "/" + "/".join(relative_path)
            
            self.request.set('request_url', path)

            logger.info("Getting views for %s between %s and %s" %
                          (path, start_date, end_date))
            renderer = getMultiAdapter(
                (self.context, self.request, report), IAnalyticsReportRenderer
            )

            data = renderer.data()
            
            if data and 'ga:pageviews' in data[0]:
                result = data[0]['ga:pageviews']
              
        return result