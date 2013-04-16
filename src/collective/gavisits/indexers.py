from plone.indexer.decorator import indexer
from plone.dexterity.interfaces import IDexterityContent

from Products.ATContentTypes.interfaces.interfaces import IATContentType

from collective.gavisits.behavior import IVisitsCounter


@indexer(IDexterityContent)
def get_visits(object, **kw):
    try:
        behavior = IVisitsCounter(object)
    except TypeError:
        raise AttributeError  # Do not index objects that do not provide the behavior

    visits = behavior.visits

    return visits


@indexer(IATContentType)
def get_visits_raise(object, **kw):
    # This is here because I don't want ATContentTypes to be indexed
    raise AttributeError
