# encoding: utf-8

from zope.globalrequest import getRequest
from collective.eeafaceted.collectionwidget.interfaces import NoCollectionWidgetDefinedException
from collective.eeafaceted.collectionwidget.utils import getCollectionLinkCriterion


CURRENT_CRITERION = 'querynextprev.current_criterion'


class CurrentCriterionProvider(object):

    """Provides key and value for current criterion in querynextprev."""

    def __init__(self, context):
        self.context = context
        self.request = getRequest()

    def get_key(self):
        return CURRENT_CRITERION

    def get_value(self):
        try:
            criterion = getCollectionLinkCriterion(self.context)
        except NoCollectionWidgetDefinedException:
            return ''
        attr = '{}[]'.format(criterion.__name__)
        return self.request.form.get(attr, '')
