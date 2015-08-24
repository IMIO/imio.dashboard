# encoding: utf-8
from plone.app.collection.config import ATCT_TOOLNAME

from Products.Archetypes.atapi import DisplayList
from Products.CMFCore.utils import getToolByName


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
        tool = getToolByName(self, ATCT_TOOLNAME)
        # default behaviour, get displayable metadata
        metadata = tool.getMetadataDisplay(exclude)
        # addtional columns, prepend a [additional] to the term value
        # so these columns are easy to locate in the vocabulary
        additional = self.additionalViewFields()
        res = []
        for k, v in additional.items():
            res.append((k, '[additional] {0}'.format(v)))
        return (metadata + DisplayList(res)).sortedByValue()

    def additionalViewFields(self):
        """See docstring in interfaces.py."""
        return DisplayList((('pretty_link', 'Pretty link'),
                            ('actions', 'Actions'),
                            ('select_row', 'Select row'), ))
