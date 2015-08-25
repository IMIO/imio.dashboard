# encoding: utf-8

from Products.Archetypes.atapi import DisplayList

from collective.eeafaceted.z3ctable.interfaces import IFacetedColumn

from zope.component import getGlobalSiteManager
from zope.i18n import translate as _


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
