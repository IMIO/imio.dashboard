# -*- coding: utf-8 -*-
"""Base module for unittesting."""

import unittest

import imio.dashboard
from collective.eeafaceted.dashboard.utils import enableFacetedDashboardFor
from plone import api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    PLONE_FIXTURE,
    TEST_USER_ID,
    TEST_USER_NAME,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
    applyProfile,
    login,
    setRoles,
)
from plone.testing import z2
from zope.globalrequest.local import setLocal


class ImioDashboardLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    products = ("imio.dashboard", "plone.restapi")

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""
        # Load ZCML
        self.loadZCML(package=imio.dashboard, name="testing.zcml")
        for p in self.products:
            z2.installProduct(app, p)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        setLocal("request", portal.REQUEST)
        # Install into Plone site using portal_setup
        applyProfile(portal, "imio.dashboard:testing")

        # Login and create some test content
        setRoles(portal, TEST_USER_ID, ["Manager"])
        login(portal, TEST_USER_NAME)
        folder_id = portal.invokeFactory("Folder", "folder", title="Folder")
        folder = portal[folder_id]
        dashboardcollection = api.content.create(
            id="dc1",
            type="DashboardCollection",
            title="Dashboard collection 1",
            container=portal,
            sort_on="",
            sort_reversed="",
        )
        dashboardcollection.query = [
            {
                "i": "portal_type",
                "o": "plone.app.querystring.operation.selection.is",
                "v": ["Folder"],
            }
        ]
        enableFacetedDashboardFor(folder, default_UID=dashboardcollection.UID())
        enableFacetedDashboardFor(folder)
        folder.reindexObject()

        # Commit so that the test browser sees these objects
        import transaction

        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        for p in reversed(self.products):
            z2.uninstallProduct(app, p)


FIXTURE = ImioDashboardLayer(name="FIXTURE")


INTEGRATION = IntegrationTesting(bases=(FIXTURE,), name="INTEGRATION")


FUNCTIONAL = FunctionalTesting(bases=(FIXTURE, z2.ZSERVER_FIXTURE), name="FUNCTIONAL")


ACCEPTANCE = FunctionalTesting(
    bases=(FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, z2.ZSERVER_FIXTURE),
    name="ACCEPTANCE",
)


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION

    def setUp(self):
        super(IntegrationTestCase, self).setUp()
        self.portal = self.layer["portal"]
        self.request = self.portal.REQUEST
        self.folder = self.portal.get("folder")
        self.faceted_table = self.folder.restrictedTraverse("faceted-table-view")


class FunctionalTestCase(IntegrationTestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL

    def setUp(self):
        super(FunctionalTestCase, self).setUp()
        import transaction

        transaction.commit()
