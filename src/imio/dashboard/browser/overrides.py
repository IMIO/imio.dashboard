# -*- coding: utf-8 -*-
from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget
from collective.eeafaceted.z3ctable.browser.views import FacetedTableView
from Products.CMFCore.utils import getToolByName

from imio.dashboard.columns import ActionsColumn


class IDFacetedTableView(FacetedTableView):

    def _manualColumnFor(self, colName):
        """Manage our own columns."""
        column = super(IDFacetedTableView, self)._manualColumnFor(colName)
        if not column:
            if colName == u'actions':
                column = ActionsColumn(self.context, self.request, self)
                column.view_name = 'actions_panel'
                column.params = {'showHistory': True, 'showActions': False}
        return column

    def _getViewFields(self):
        """Returns fields we want to show in the table."""
        colNames = ['Title', 'CreationDate', 'Creator', 'review_state', 'getText']
        # if we can get the collection we are working with,
        # use customViewFields defined on it if any
        for criterion in self.criteria.values():
            if criterion.widget == CollectionWidget.widget_type:
                # value is stored in the request with ending [], like 'c4[]'
                collectionUID = self.request.get('{0}[]'.format(criterion.getId()))
                catalog = getToolByName(self.context, 'portal_catalog')
                collection = catalog(UID=collectionUID)
                if collection:
                    collection = collection[0].getObject()
                    customViewFields = collection.getCustomViewFields()
                    if customViewFields:
                        colNames = customViewFields
        return colNames

