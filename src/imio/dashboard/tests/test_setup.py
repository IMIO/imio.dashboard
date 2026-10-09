# -*- coding: utf-8 -*-
from imio.dashboard.testing import IntegrationTestCase
from plone import api
from plone.base.utils import get_installer


class TestInstall(IntegrationTestCase):
    """Test installation of imio.dashboard into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal, self.layer["request"])

    def test_product_installed(self):
        """Test if imio.dashboard is installed."""
        self.assertTrue(self.installer.is_product_installed("imio.dashboard"))

    def test_uninstall(self):
        """Test if imio.dashboard is cleanly uninstalled."""
        from imio.dashboard.interfaces import IImioDashboardLayer
        from plone.browserlayer import utils

        self.installer.uninstall_product("imio.dashboard")
        self.assertFalse(self.installer.is_product_installed("imio.dashboard"))
        self.assertNotIn(IImioDashboardLayer, utils.registered_layers())
        self.assertIsNone(
            api.portal.get_registry_record(
                "plone.bundles/imio-dashboard.jscompilation", default=None
            )
        )

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IImioDashboardLayer is registered."""
        from imio.dashboard.interfaces import IImioDashboardLayer
        from plone.browserlayer import utils

        self.assertIn(IImioDashboardLayer, utils.registered_layers())

    # registry.xml
    def test_resources(self):
        """Test that the imio.dashboard JS bundle is registered after the faceted one."""
        prefix = "plone.bundles/imio-dashboard."
        js = api.portal.get_registry_record(prefix + "jscompilation")
        self.assertEqual(js, "++resource++imio.dashboard/imio.dashboard.js")
        self.assertEqual(
            api.portal.get_registry_record(prefix + "depends"), "faceted.view"
        )
        self.assertTrue(api.portal.get_registry_record(prefix + "enabled"))
        self.assertTrue(self.portal.unrestrictedTraverse(js))

    # registry.xml
    def test_types_not_searched(self):
        """Test that the dashboard and POD types are not searched."""
        types_not_searched = api.portal.get_registry_record("plone.types_not_searched")
        for portal_type in (
            "Collection",
            "DashboardCollection",
            "ConfigurablePODTemplate",
            "DashboardPODTemplate",
            "PODTemplate",
            "StyleTemplate",
            "SubTemplate",
        ):
            self.assertIn(portal_type, types_not_searched)

    # rolemap.xml
    def test_rolemap(self):
        """Test that only the Manager can configure the faceted navigation."""
        permission = "eea.facetednavigation: Configure faceted"
        roles = [
            role["name"]
            for role in self.portal.rolesOfPermission(permission)
            if role["selected"]
        ]
        self.assertEqual(roles, ["Manager"])
        self.assertFalse(self.portal.acquiredRolesAreUsedBy(permission))

    # metadata.xml
    def test_dependencies(self):
        """Test that the dependency profiles are installed."""
        setup_tool = api.portal.get_tool("portal_setup")
        for profile in (
            "collective.eeafaceted.dashboard:default",
            "collective.eeafaceted.batchactions:default",
            "imio.actionspanel:default",
        ):
            self.assertNotEqual(
                setup_tool.getLastVersionForProfile(profile), "unknown", profile
            )
