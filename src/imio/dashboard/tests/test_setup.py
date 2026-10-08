# -*- coding: utf-8 -*-
from imio.dashboard.testing import IntegrationTestCase
from plone import api


class TestInstall(IntegrationTestCase):
    """Test installation of imio.dashboard into Plone."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = api.portal.get_tool("portal_quickinstaller")

    def test_product_installed(self):
        """Test if imio.dashboard is installed with portal_quickinstaller."""
        self.assertTrue(self.installer.isProductInstalled("imio.dashboard"))

    def test_uninstall(self):
        """Test if imio.dashboard is cleanly uninstalled."""
        self.installer.uninstallProducts(["imio.dashboard"])
        self.assertFalse(self.installer.isProductInstalled("imio.dashboard"))

    # browserlayer.xml
    def test_browserlayer(self):
        """Test that IImioDashboardLayer is registered."""
        from imio.dashboard.interfaces import IImioDashboardLayer
        from plone.browserlayer import utils

        self.assertIn(IImioDashboardLayer, utils.registered_layers())

    # jsregistry.xml
    def test_resources(self):
        """Test that the imio.dashboard JS is registered."""
        resource_ids = api.portal.get_tool("portal_javascripts").getResourceIds()
        self.assertIn("++resource++imio.dashboard/imio.dashboard.js", resource_ids)

    # propertiestool.xml
    def test_types_not_searched(self):
        """Test that the dashboard and POD types are not searched."""
        types_not_searched = api.portal.get_tool(
            "portal_properties"
        ).site_properties.types_not_searched
        for portal_type in (
            "Collection",
            "DashboardCollection",
            "Topic",
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
