# -*- coding: utf-8 -*-
"""Base module for unittesting."""

from collective.eeafaceted.dashboard.utils import enableFacetedDashboardFor
from imio.helpers.catalog import addOrUpdateIndexes
from plone import api
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from plone.testing import z2
from zope.globalrequest.local import setLocal

import imio.dashboard
import os
import unittest


class ImioDashboardLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)
    products = ("imio.dashboard",)

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
        portal[folder_id].reindexObject()

        # Commit so that the test browser sees these objects
        import transaction

        transaction.commit()

    def tearDownZope(self, app):
        """Tear down Zope."""
        for p in reversed(self.products):
            z2.uninstallProduct(app, p)


FIXTURE = ImioDashboardLayer(name="FIXTURE")


INTEGRATION = IntegrationTesting(bases=(FIXTURE,), name="INTEGRATION")


FUNCTIONAL = FunctionalTesting(bases=(FIXTURE,), name="FUNCTIONAL")


class CombinedIndexDashboardLayer(ImioDashboardLayer):
    """Robot data: the content of test_combined_index, dashboard `folder` with the c10/c11 criteria
    of combined_index_widgets.xml on contained_types_and_states, its default collection lists the Folders.
    Not based on FIXTURE: a stacked registry hides the z3ctable columns from the c.e.dashboard
    customViewFields vocabulary (gsm.registeredAdapters())."""

    def setUpPloneSite(self, portal):
        super(CombinedIndexDashboardLayer, self).setUpPloneSite(portal)
        addOrUpdateIndexes(portal, {"contained_types_and_states": ("KeywordIndex", {})})
        wf_tool = portal.portal_workflow
        wf_tool.setDefaultChain("simple_publication_workflow")
        # the collection is in the dashboard: contained_types_and_states needs its review_state
        wf_tool.setChainForPortalTypes(
            ["DashboardCollection"], ("simple_publication_workflow",)
        )
        folder = portal.folder
        collection = api.content.create(
            container=folder,
            type="DashboardCollection",
            id="dc1",
            title="Folders",
            sort_on="",
            sort_reversed="",
        )
        collection.query = [
            {
                "i": "portal_type",
                "o": "plone.app.querystring.operation.selection.is",
                "v": ["Folder"],
            }
        ]
        collection.customViewFields = (u"Title",)
        collection.reindexObject()
        folder1 = api.content.create(
            container=portal, type="Folder", id="folder1", title="Folder 1"
        )
        api.content.create(
            container=folder1,
            type="Document",
            id="privatedoc",
            title="Private document",
        )
        doc = api.content.create(
            container=folder1,
            type="Document",
            id="publicdoc",
            title="Published document",
        )
        api.content.transition(doc, "publish")
        folder2 = api.content.create(
            container=portal, type="Folder", id="folder2", title="Folder 2"
        )
        folder3 = api.content.create(
            container=portal, type="Folder", id="folder3", title="Folder 3"
        )
        api.content.create(
            container=folder3, type="Folder", id="privatefolder", title="Private folder"
        )
        api.content.create(
            container=folder3,
            type="Document",
            id="privatedoc2",
            title="Private document 2",
        )
        for obj in (folder1, folder2, folder3):
            obj.reindexObject(idxs=["contained_types_and_states"])
        xmlpath = os.path.join(
            os.path.dirname(__file__),
            "tests",
            "faceted_conf",
            "combined_index_widgets.xml",
        )
        enableFacetedDashboardFor(folder, xmlpath=xmlpath, default_UID=collection.UID())


COMBINED_INDEX_FIXTURE = CombinedIndexDashboardLayer(name="COMBINED_INDEX_FIXTURE")


try:  # Plone 5.2+
    from plone.testing.zope import WSGI_SERVER_FIXTURE as SERVER_FIXTURE
except ImportError:  # Plone 4
    SERVER_FIXTURE = z2.ZSERVER_FIXTURE


# robot scenarios (tests/robot), served over HTTP
ACCEPTANCE = FunctionalTesting(
    bases=(COMBINED_INDEX_FIXTURE, REMOTE_LIBRARY_BUNDLE_FIXTURE, SERVER_FIXTURE),
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
        enableFacetedDashboardFor(self.folder)
        self.faceted_table = self.folder.restrictedTraverse("faceted-table-view")


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL
