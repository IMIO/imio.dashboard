# -*- coding: utf-8 -*-
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.schema.interfaces import IVocabularyFactory
from Products.CMFCore.utils import getToolByName
from plone.app.testing import login
from plone import api
from imio.dashboard.testing import IntegrationTestCase
from eea.facetednavigation.interfaces import IFacetedNavigable


class TestConditionAwareVocabulary(IntegrationTestCase):
    """Test the ConditionAwareCollectionVocabulary vocabulary."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        # make sure we have a default workflow
        self.wfTool = self.portal.portal_workflow
        self.wfTool.setDefaultChain('simple_publication_workflow')
        self.folder = api.content.create(id='f', type='Folder', title='My category', container=self.portal)
        self.dashboardcollection = api.content.create(
            id='dc1',
            type='DashboardCollection',
            title='Dashboard collection 1',
            container=self.folder
        )
        alsoProvides(self.folder, IFacetedNavigable)

    def test_creatorsvocabulary(self):
        """This will return every users that created a content in the portal."""
        factory = queryUtility(IVocabularyFactory, u'imio.dashboard.creatorsvocabulary')
        self.assertEquals(len(factory(self.portal)), 1)
        self.assertTrue('test_user_1_' in factory(self.portal))
        # no fullname, title is the login
        self.assertEquals(factory(self.portal).getTerm('test_user_1_').title, 'test_user_1_')
        # add another user, create content and test again
        membershipTool = getToolByName(self.portal, 'portal_membership')
        membershipTool.addMember('test_user_2_', 'password', ['Manager'], [])
        user2 = membershipTool.getMemberById('test_user_2_')
        user2.setMemberProperties({'fullname': 'User 2'})
        self.assertEquals(user2.getProperty('fullname'), 'User 2')
        login(self.portal, 'test_user_2_')
        # vocabulary cache not cleaned
        self.assertEquals(len(factory(self.portal)), 1)
        self.portal.invokeFactory('Folder', id='folder2')
        # vocabulary cache cleaned
        self.assertEquals(len(factory(self.portal)), 2)
        self.assertEquals(factory(self.portal).getTerm('test_user_2_').title, 'User 2')
