# -*- coding: utf-8 -*-

from imio.dashboard.columns import ActionsColumn
from imio.dashboard.testing import IntegrationTestCase


class TestColumns(IntegrationTestCase):

    def test_ActionsColumn(self):
        """Render the @@actions_panel view."""
        table = self.faceted_table
        column = ActionsColumn(self.portal, self.portal.REQUEST, table)
        brain = self.portal.portal_catalog(UID=self.folder.UID())[0]
        # it is a BrowserViewCallColumn with some fixed parameters
        self.assertEquals(column.view_name, 'actions_panel')
        rendered_column = column.renderCell(brain)
        # common parts are there : 'edit', 'Delete', 'history'
        self.assertIn("/edit", rendered_column)
        self.assertIn("javascript:confirmDeleteObject", rendered_column)
        self.assertIn("history.gif", rendered_column)
