# -*- coding: utf-8 -*-
from eea.facetednavigation.interfaces import IFacetedNavigable
from imio.dashboard.testing import IntegrationTestCase
from imio.dashboard.vocabulary import HAS_PLONEGROUP
from plone import api
from plone.app.testing import login
from Products.CMFCore.utils import getToolByName
from zope.component import queryUtility
from zope.interface import alsoProvides
from zope.schema.interfaces import IVocabularyFactory


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
        self.assertEqual(len(factory(self.portal)), 1)
        self.assertTrue('test_user_1_' in factory(self.portal))
        # no fullname, title is the login
        self.assertEqual(factory(self.portal).getTerm('test_user_1_').title, 'test_user_1_')
        # add another user, create content and test again
        membershipTool = getToolByName(self.portal, 'portal_membership')
        membershipTool.addMember('test_user_2_', 'password', ['Manager'], [])
        user2 = membershipTool.getMemberById('test_user_2_')
        user2.setMemberProperties({'fullname': 'User 2'})
        self.assertEqual(user2.getProperty('fullname'), 'User 2')
        login(self.portal, 'test_user_2_')
        # vocabulary cache not cleaned
        self.assertEqual(len(factory(self.portal)), 1)
        self.portal.invokeFactory('Folder', id='folder2')
        # vocabulary cache cleaned
        self.assertEqual(len(factory(self.portal)), 2)
        self.assertEqual(factory(self.portal).getTerm('test_user_2_').title, 'User 2')


class TestContactsReviewStatesVocabulary(IntegrationTestCase):
    """Test the ContactsReviewStatesVocabulary vocabulary."""

    def test_call(self):
        factory = queryUtility(IVocabularyFactory, u'imio.dashboard.ContactsReviewStatesVocabulary')
        wf_tool = self.portal.portal_workflow
        wf_tool.setChainForPortalTypes(('organization', 'person', 'held_position'), '', verify=False)
        self.assertEqual(len(factory(self.portal)), 0)
        # states of the 3 contact types workflows, without duplicates
        wf_tool.setChainForPortalTypes(('organization', ), 'simple_publication_workflow', verify=False)
        wf_tool.setChainForPortalTypes(('person', ), 'one_state_workflow', verify=False)
        wf_tool.setChainForPortalTypes(('held_position', ), 'simple_publication_workflow', verify=False)
        self.assertEqual(sorted([(term.value, term.token, term.title) for term in factory(self.portal)]),
                         [('pending', 'pending', u'Pending review'),
                          ('private', 'private', u'Private'),
                          ('published', 'published', u'Published')])


class TestPloneGroupInterfacesVocabulary(IntegrationTestCase):
    """Test the PloneGroupInterfacesVocabulary vocabulary."""

    def test_call(self):
        factory = queryUtility(IVocabularyFactory, u'imio.dashboard.PloneGroupInterfacesVocabulary')
        # collective.contact.plonegroup is not installed
        self.assertFalse(HAS_PLONEGROUP)
        self.assertEqual(len(factory(self.portal)), 0)
