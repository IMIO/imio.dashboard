# -*- coding: utf-8 -*-
from zope.component import queryUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.CMFCore.utils import getToolByName
from plone.app.testing import login
from plone import api
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

    def test_conditionawarecollectionvocabulary(self):
        """This vocabulary is condition aware, it means
           that it will take into account condition defined in the
           'tal_condition' field added by ITALConditionable."""
        self.assertTrue(ITALConditionable.providedBy(self.dashboardcollection))
        factory = queryUtility(IVocabularyFactory, u'imio.dashboard.conditionawarecollectionvocabulary')
        # for now, no condition defined on the collection so it is in the vocabulary
        self.assertTrue(not self.dashboardcollection.tal_condition)
        vocab = factory(self.portal)
        self.assertTrue(self.dashboardcollection.UID() in [term.token for term in vocab])
        # now define a condition and by pass for Manager
        self.dashboardcollection.tal_condition = u'python:False'
        self.dashboardcollection.roles_bypassing_talcondition = [u"Manager"]
        # No more listed except for Manager
        vocab = factory(self.portal)
        self.assertTrue(self.dashboardcollection.UID() in [term.token for term in vocab])
        # Now, desactivate by pass for manager
        self.dashboardcollection.roles_bypassing_talcondition = []
        vocab = factory(self.portal)
        self.assertTrue(not self.dashboardcollection.UID() in [term.token for term in vocab])
        # If condition is True, it is listed
        self.dashboardcollection.tal_condition = u'python:True'
        vocab = factory(self.portal)
        self.assertTrue(self.dashboardcollection.UID() in [term.token for term in vocab])

    def test_creatorsvocabulary(self):
        """This will return every users that created a content in the portal."""
        factory = queryUtility(IVocabularyFactory, u'imio.dashboard.creatorsvocabulary')
        self.assertEquals(len(factory(self.portal)), 1)
        self.assertTrue("test_user_1_" in factory(self.portal))
        # add another user, create content and test again
        membershipTool = getToolByName(self.portal, 'portal_membership')
        membershipTool.addMember('test_user_2_', 'password', ['Manager'], [])
        login(self.portal, 'test_user_2_')
        # vocabulary cache not cleaned
        self.assertEquals(len(factory(self.portal)), 1)
        self.portal.invokeFactory('Folder', id='folder2')
        # vocabulary cache cleaned
        self.assertEquals(len(factory(self.portal)), 2)
