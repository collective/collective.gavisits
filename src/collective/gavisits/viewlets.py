
from plone.app.layout.viewlets import ViewletBase

from collective.gavisits.behavior import IVisitsCounter


class VisitsCounter(ViewletBase):
    """ This viewlet will render a visit counter for the given object
    """

    def available(self):
        try:
            IVisitsCounter(self.context)
            return True
        except TypeError:
            return False

    def get_visits(self):
        return IVisitsCounter(self.context).visits
