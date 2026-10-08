# -*- coding: utf-8 -*-
from imio.dashboard.testing import IntegrationTestCase
from zope.i18n import translate


class TestLocales(IntegrationTestCase):
    """Test the translations shipped by imio.dashboard."""

    def test_translations(self):
        self.assertEqual(translate(u'Organizations searches', domain='imio.dashboard', target_language='fr'),
                         u'Recherches organisations')
        self.assertEqual(translate(u'Contact plonegroup/normal', domain='eea', target_language='fr'),
                         u'Défini dans')
        self.assertEqual(translate(u'header_actions', domain='collective.eeafaceted.z3ctable', target_language='fr'),
                         u'Actions')
