# -*- coding: utf-8 -*-
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from imio.dashboard.testing import IntegrationTestCase
from collective.behavior.talcondition.interfaces import ITALConditionable


class TestConditionAwareVocabulary(IntegrationTestCase):
    """Test the ConditionAwareCollectionVocabulary vocabulary."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.dashboardcollection = api.content.create(
            id='dc1',
            type='DashboardCollection',
            title='Dashboard collection 1',
            container=self.portal
        )

    def test_vocabulary(self):
        """This vocabulary is condition aware, it means
           that it will take into account condition defined in the
           'tal_condition' field added by ITALConditionable."""
        self.assertTrue(ITALConditionable.providedBy(self.dashboardcollection))
        factory = queryUtility(IVocabularyFactory, u'imio.dashboard.conditionawarecollectionvocabulary')
        # for now, no condition defined on the collection so it is in the vocabulary
        self.assertTrue(not self.dashboardcollection.tal_condition)
        vocab = factory(self.portal)
        self.assertTrue(self.dashboardcollection.UID() in vocab)
        # now define a condition
        self.dashboardcollection.tal_condition = u'python:False'
        # No more listed except for Manager
        vocab = factory(self.portal)
        self.assertTrue(self.dashboardcollection.UID() in vocab)
        # Now, desactivate manager role
        setRoles(self.portal, TEST_USER_ID, [''])
        vocab = factory(self.portal)
        self.assertTrue(not self.dashboardcollection.UID() in vocab)
        # If condition is True, it is listed
        self.dashboardcollection.tal_condition = u'python:True'
        vocab = factory(self.portal)
        self.assertTrue(self.dashboardcollection.UID() in vocab)
        # Last, reactivate manager role
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
