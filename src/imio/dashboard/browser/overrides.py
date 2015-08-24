# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone.app.collection.interfaces import ICollection

from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget
from collective.eeafaceted.z3ctable.browser.views import FacetedTableView
from collective.eeafaceted.z3ctable.columns import BrowserViewCallColumn
from collective.eeafaceted.z3ctable.columns import CheckBoxColumn
from imio.dashboard.columns import PrettyLinkColumn


class IDFacetedTableView(FacetedTableView):

    def _manualColumnFor(self, colName):
        """Manage our own columns."""
        column = super(IDFacetedTableView, self)._manualColumnFor(colName)
        if not column:
            if colName == u'actions':
                column = BrowserViewCallColumn(self.context, self.request, self)
                column.header_js = '<script type="text/javascript">jQuery(document).ready(initializeOverlays);' \
                                   'jQuery(document).ready(preventDefaultClickTransition);</script>'
                column.view_name = 'actions_panel'
                column.params = {'showHistory': True, 'showActions': False}
            if colName == u'pretty_link':
                column = PrettyLinkColumn(self.context, self.request, self)
            if colName == u'select_row':
                column = CheckBoxColumn(self.context, self.request, self)
        return column

    def _getViewFields(self):
        """Returns fields we want to show in the table."""
        colNames = ['Title', 'CreationDate', 'Creator', 'review_state', 'getText']
        # if the context is a collection, get customViewFields on it
        collection = None
        if ICollection.providedBy(self.context):
            collection = self.context
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
                        collection = collection[0].getObject()
        if collection:
            customViewFields = collection.getCustomViewFields()
            if customViewFields:
                colNames = customViewFields

        return colNames
