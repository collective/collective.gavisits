# -*- coding: utf-8 -*-

from zope import schema
from zope.component import adapts
from zope.interface import alsoProvides

from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.directives import form

from collective.gavisits import _


class IVisitsCounter(form.Schema):

    visits = schema.Int(
        title=_(u'label_visits', default=u'Visits'),
        description=_(u'help_visits',
                          default=u'Number of visits for this element.'),
        required=False,
        )

    directives.omitted('visits')


alsoProvides(IVisitsCounter, IFormFieldProvider)


class VisitsCounter(object):
    """
    """
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    def _get_visits(self):
        visits = getattr(self.context, 'visits', 0)
        return visits

    def _set_visits(self, value):
        if not value:
            value = 0

        if not isinstance(value, int):
            raise ValueError('Visits must be an integer.')
        self.context.visits = value

    visits = property(_get_visits, _set_visits)
