# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.app.collection.interfaces import ICollection

from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget
from collective.eeafaceted.z3ctable.browser.views import FacetedTableView


class IDFacetedTableView(FacetedTableView):

    def __init__(self, context, request):
        super(IDFacetedTableView, self).__init__(context, request)
        self.collection = self._set_collection()

    def _set_collection(self):
        if ICollection.providedBy(self.context):
            return self.context
        else:
            # if we can get the collection we are working with,
            # use customViewFields defined on it if any
            for criterion in self.criteria.values():
                if criterion.widget == CollectionWidget.widget_type:
                    # value is stored in the request with ending [], like 'c4[]'
                    collectionUID = self.request.get('{0}[]'.format(criterion.getId()))
                    catalog = getToolByName(self.context, 'portal_catalog')
                    collection = catalog(UID=collectionUID)
                    if collection:
                        return collection[0].getObject()

    def _getViewFields(self):
        """Returns fields we want to show in the table."""

        # if the context is a collection, get customViewFields on it
        if self.collection:
            return self.collection.getCustomViewFields()

        # else get default column names
        return super(IDFacetedTableView, self)._getViewFields()

    def orderColumns(self):
        """ Order columns of the table."""
        # do this to keep the column ordered as found on the field
        # 'customViewFields' of the collection if there is any
        if self.collection:
            for i, column in enumerate(self.columns):
                column.weight = i

        super(IDFacetedTableView, self).orderColumns()
