# -*- coding: utf-8 -*-
from collective.eeafaceted.z3ctable.interfaces import IFacetedColumn
from imio.dashboard.columns import ContactPrettyLinkColumn
from imio.dashboard.interfaces import IContactsDashboard
from imio.dashboard.testing import IntegrationTestCase
from plone import api
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class DummyContact(object):
    def get_full_title(self):
        return u"Organization - Sub organization"


class TestContactPrettyLinkColumn(IntegrationTestCase):
    """Test the 'pretty_link' column of the contacts dashboards."""

    def setUp(self):
        super(TestContactPrettyLinkColumn, self).setUp()
        alsoProvides(self.folder, IContactsDashboard)
        self.column = getMultiAdapter(
            (self.folder, self.request, self.faceted_table),
            IFacetedColumn,
            name="pretty_link",
        )

    def test_contentValue(self):
        self.assertIsInstance(self.column, ContactPrettyLinkColumn)
        self.assertEqual(
            self.column.contentValue(DummyContact()), u"Organization - Sub organization"
        )
        self.assertEqual(self.column.params["target"], "_blank")
        self.assertEqual(self.column.params["additionalCSSClasses"], ["link-tooltip"])

    def test_getCSSClasses(self):
        brain = api.content.find(UID=self.folder.UID())[0]
        # not an organization: no organizations chain class
        self.assertEqual(self.column.getCSSClasses(brain)["td"], "pretty_link")
