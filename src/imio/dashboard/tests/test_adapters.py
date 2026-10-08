# -*- coding: utf-8 -*-
from collective.eeafaceted.collectionwidget.utils import getCollectionLinkCriterion
from eea.facetednavigation.interfaces import ICriteria
from imio.dashboard.adapters import CURRENT_CRITERION
from imio.dashboard.adapters import CurrentCriterionProvider
from imio.dashboard.testing import IntegrationTestCase


class TestCurrentCriterionProvider(IntegrationTestCase):
    """Test the querynextprev current criterion provider."""

    def test_get_key(self):
        self.assertEqual(CurrentCriterionProvider(self.folder).get_key(), 'querynextprev.current_criterion')
        self.assertEqual(CURRENT_CRITERION, 'querynextprev.current_criterion')

    def test_get_value(self):
        provider = CurrentCriterionProvider(self.folder)
        # no collection selected
        self.assertEqual(provider.get_value(), '')
        # selected collection UID
        criterion = getCollectionLinkCriterion(self.folder)
        self.request.form['{0}[]'.format(criterion.__name__)] = 'collection_uid'
        self.assertEqual(provider.get_value(), 'collection_uid')
        # no collection widget
        ICriteria(self.folder).delete(criterion.__name__)
        self.assertEqual(provider.get_value(), '')
