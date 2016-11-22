# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from Products.Archetypes import atapi
from Products.Archetypes.atapi import registerType
from Products.Archetypes.Field import BooleanField
from Products.Archetypes.Widget import BooleanWidget
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from plone.app.collection.collection import Collection, CollectionSchema
from plone.app.collection.config import ATCT_TOOLNAME
from plone.app.querystring.queryparser import parseFormquery
from imio.dashboard.config import PROJECTNAME
from imio.dashboard.interfaces import ICustomViewFieldsVocabulary
from imio.dashboard.interfaces import IDashboardCollection
from imio.dashboard import ImioDashboardMessageFactory as _


DashboardCollectionSchema = CollectionSchema.copy() + atapi.Schema((
    BooleanField(
        name="showNumberOfItems",
        required=False,
        widget=BooleanWidget(
            label=_(u'Show number of items in filter'),
        ),
        schemata="default",
    ),
))

# hide these fields to avoid conflict with eea.facetednavigation parameters
DashboardCollectionSchema['limit'].default = 0
DashboardCollectionSchema['b_size'].widget.visible = -1
DashboardCollectionSchema['limit'].widget.visible = -1


class DashboardCollection(Collection):
    """A Collection used in our dashboards"""
    implements(IDashboardCollection)
    meta_type = "DashboardCollection"
    schema = DashboardCollectionSchema
    security = ClassSecurityInfo()

    security.declareProtected(View, 'listMetaDataFields')

    def listMetaDataFields(self, exclude=True):
        """
          Return a list of metadata fields from portal_catalog.
          Wrap the vocabulary in an adapter so it can be easily overrided by another package
          this is made so a package can add it's own custom columns, not only metadata.
        """
        return ICustomViewFieldsVocabulary(self).listMetaDataFields(exclude=exclude)

    security.declareProtected(View, 'selectedViewFields')

    def selectedViewFields(self):
        """
          Get which metadata field are selected.
          Override as it is used by the tabular_view and there, we do not display
          the additional fields or it breaks the view."""
        tool = getToolByName(self, ATCT_TOOLNAME)
        metadatas = [metadata.index for metadata in tool.getEnabledMetadata()]
        _mapping = {}
        for field in self.listMetaDataFields().items():
            if not field[0] in metadatas:
                continue
            _mapping[field[0]] = field
        return [_mapping[field] for field in self.customViewFields if field in metadatas]

    security.declareProtected(View, 'selectedViewFields')

    def displayCatalogQuery(self):
        """
          Return the stored query as a readable catalog query."""
        return parseFormquery(self, self.query)


registerType(DashboardCollection, PROJECTNAME)
