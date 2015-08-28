# encoding: utf-8

from Products.Archetypes.atapi import DisplayList

from collective.eeafaceted.z3ctable.interfaces import IFacetedColumn

from zope.component import getGlobalSiteManager
from zope.i18n import translate as _

from imio.dashboard.utils import getCollectionLinkCriterion


CURRENT_CRITERION = 'querynextprev.current_criterion'


class CustomViewFieldsVocabularyAdapter(object):
    """Handles plone.app.collection Collection.customViewFields field vocabulary.
       By default it has the same behaviour as original one but you can override the
       additionalViewFields method to provide your own fields.
    """

    def __init__(self, context):
        self.context = context
        self.request = self.context.REQUEST

    def listMetaDataFields(self, exclude=True):
        """See docstring in interfaces.py."""

        gsm = getGlobalSiteManager()
        columns = [adapter.name for adapter in list(gsm.registeredAdapters())
                   if issubclass(adapter.provided, IFacetedColumn)]

        vocabulary = DisplayList(
            [(name, _(name, 'collective.eeafaceted.z3ctable', context=self.request)) for name in columns]
        ).sortedByValue()

        return vocabulary


class CurrentCriterionProvider(object):

    """Provides key and value for current criterion in querynextprev."""

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    def get_key(self):
        return CURRENT_CRITERION

    def get_value(self):
        criterion = getCollectionLinkCriterion(self.context)
        if criterion is not None:
            attr = '{}[]'.format(criterion.__name__)
            return self.request.form.get(attr, '')
        else:
            return ''
