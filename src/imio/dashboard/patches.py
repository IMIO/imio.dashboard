# encoding: utf-8
# monkey patches

from Products.CMFCore.utils import getToolByName
from plone.app.collection.config import ATCT_TOOLNAME
from imio.dashboard.interfaces import ICustomViewFieldsVocabulary


# monkey patch the plone.app.collection collection.listMetaDataFields
# to wrap the vocabulary in an adapter so it can be easily overrided by another package
# this is made so a package can add it's own custom columns, not only metadata
def listMetaDataFields(self, exclude=True):
    """Return a list of metadata fields from portal_catalog.
    """
    return ICustomViewFieldsVocabulary(self).listMetaDataFields(exclude=exclude)


# override the selectedViewFields that is used by the tabular_view to not display
# the additional fields or it breaks the view
def selectedViewFields(self):
    """Get which metadata field are selected"""
    tool = getToolByName(self, ATCT_TOOLNAME)
    metadatas = [metadata.index for metadata in tool.getEnabledMetadata()]

    _mapping = {}
    for field in self.listMetaDataFields().items():
        if not field[0] in metadatas:
            continue
        _mapping[field[0]] = field
    return [_mapping[field] for field in self.customViewFields if field in metadatas]
