# -*- coding: utf-8 -*-
from imio.dashboard.testing import IntegrationTestCase
from zope.i18n import translate


class TestLocales(IntegrationTestCase):
    """Test the translations shipped by imio.dashboard."""

    def test_translations(self):
        self.assertEqual(
            translate(
                "Organizations searches", domain="imio.dashboard", target_language="fr"
            ),
            "Recherches organisations",
        )
        self.assertEqual(
            translate("Contact plonegroup/normal", domain="eea", target_language="fr"),
            "Défini dans",
        )
        self.assertEqual(
            translate(
                "header_actions",
                domain="collective.eeafaceted.z3ctable",
                target_language="fr",
            ),
            "Actions",
        )
