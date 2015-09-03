# -*- coding: utf-8 -*-

from imio.dashboard.columns import ActionsColumn
from imio.dashboard.columns import PrettyLinkColumn
from imio.dashboard.testing import IntegrationTestCase


class TestColumns(IntegrationTestCase):

    def test_PrettyLinkColumn(self):
        """Test the PrettyLinkColumn, it will render IPrettyLink.getLink."""
        table = self.faceted_table
        column = PrettyLinkColumn(self.portal, self.portal.REQUEST, table)
        column.attrName = 'Title'
        table.nameColumn(column, 'Title')
        # we will use the 'folder' as a brain
        brain = self.portal.portal_catalog(UID=self.folder.UID())[0]
        self.assertEquals(column.renderCell(brain),
                          u"<a class='pretty_link' title='' href='http://nohost/plone/folder' target='_self'>"
                          u"<span class='pretty_link_content'>Folder</span></a>")
        # a pretty_link class is defined for the tg
        self.assertEquals(column.cssClasses, {'td': 'pretty_link', 'th': 'th_header_Title'})

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
