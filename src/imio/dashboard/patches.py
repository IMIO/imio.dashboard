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


# override the imio.actionspanel.browser.views buildExactReferer
# to take into account the QUERY_STRING while getting the referer so
# changing an element's state will send the user back to the right page on the dashboard
def buildExactReferer(self):
    """
      Keep the exact referer.  By default, we keep 'HTTP_REFERER' but this
      is made to be overriden...
    """
    if self.request['URL'].endswith('@@faceted_query'):
        # we are displaying the actions_panel in a dashboard
        import urllib2
        return urllib2.quote('{0}#{1}'.format(self.request['HTTP_REFERER'], self.request['QUERY_STRING']))
    return self.request['HTTP_REFERER']
