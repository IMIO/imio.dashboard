# -*- coding: utf-8 -*-
from collective.eeafaceted.z3ctable.browser.views import FacetedTableView
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
