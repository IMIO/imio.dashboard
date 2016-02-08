# -*- coding: utf-8 -*-
"""Setup/installation tests for this package."""

import os
from plone import api
from eea.facetednavigation.interfaces import ICriteria
from imio.dashboard.config import COMBINED_INDEX_PREFIX
from imio.dashboard.testing import IntegrationTestCase
from imio.dashboard.tests.indexes import contained_types_and_states
from imio.dashboard.utils import getCollectionLinkCriterion


class TestCombinedIndex(IntegrationTestCase):
    """Test the Combined index functionnality."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        super(TestCombinedIndex, self).setUp()
        # add the 'contained_types_and_states' to portal_catalog
        import ipdb; ipdb.set_trace()
        # make sure we have a default workflow
        self.portal.portal_workflow.setDefaultChain('simple_publication_workflow')
        self.dashboardcollection = api.content.create(
            id='dc1',
            type='DashboardCollection',
            title='Dashboard collection 1',
            container=self.portal
        )
        # this will by default query Folders
        self.dashboardcollection.query = [
            {'i': 'portal_type',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': ['Folder', ]},
        ]
        # create 3 folders :
        # - first is empty;
        # - second contains one private Document and one published Document;
        # - third contains a private Folder.

        # folder1
        self.folder1 = api.content.create(
            id='folder1',
            type='Folder',
            title='Folder 1',
            container=self.portal
        )
        self.privatedoc = api.content.create(
            id='privatedoc',
            type='Document',
            title='Private document',
            container=self.portal.folder1
        )
        self.publicdoc = api.content.create(
            id='publicdoc',
            type='Document',
            title='Published document',
            container=self.portal.folder1
        )
        api.content.transition(self.publicdoc, 'publish')
        # folder2
        self.folder2 = api.content.create(
            id='folder2',
            type='Folder',
            title='Folder 2',
            container=self.portal
        )
        # folder3
        self.folder3 = api.content.create(
            id='folder3',
            type='Folder',
            title='Folder 3',
            container=self.portal
        )
        self.privatefolder = api.content.create(
            id='privatefolder',
            type='Folder',
            title='Private folder',
            container=self.portal.folder3
        )
        self.privatedoc2 = api.content.create(
            id='privatedoc2',
            type='Document',
            title='Private document 2',
            container=self.portal.folder3
        )
        # first check that contained_types_and_states index is correct
        self.assertEquals(contained_types_and_states(self.folder1)(),
                          ['Document', 'Document__private', 'Document__published',
                           'private', 'published'])
        self.assertEquals(contained_types_and_states(self.folder2)(), [])
        self.assertEquals(contained_types_and_states(self.folder3)(),
                          ['Document', 'Document__private',
                           'Folder', 'Folder__private', 'private'])

    def test_combined_index(self):
        """We made an index that index portal_type and review_state
           of contained elements, here we will query folders containing
           'Document' in state 'private'."""
        # set a correct collection in the REQUEST
        criterion = getCollectionLinkCriterion(self.folder)
        criterion_name = '{0}[]'.format(criterion.__name__)
        self.request.form[criterion_name] = self.dashboardcollection.UID()
        # add new widgets
        # c10 and c11 widgets are missing for now
        self.assertFalse(ICriteria(self.folder).get('c10'))
        self.assertFalse(ICriteria(self.folder).get('c11'))
        xmlpath = os.path.dirname(__file__) + '/faceted_conf/combined_index_widgets.xml'
        self.folder.unrestrictedTraverse('@@faceted_exportimport').import_xml(
            import_file=open(xmlpath))
        self.assertEquals(ICriteria(self.folder).get('c10').index,
                          u'contained_types_and_states')
        self.assertEquals(ICriteria(self.folder).get('c11').index,
                          COMBINED_INDEX_PREFIX + u'contained_types_and_states')
        # by default the dashboardcollection will return the every found folders, aka 6
        faceted_query = self.folder.restrictedTraverse('@@faceted_query')
        self.assertEquals(len(faceted_query.query()), 5)

        # filter on 'review_state', get the private elements
        self.request.form['c11[]'] = 'private'
        # we get folder1 and folder3
        uids = [brain.UID for brain in faceted_query.query()]
        self.assertTrue(self.folder1.UID() in uids and
                        self.folder3.UID() in uids)
        # filter on 'portal_type', get 'Document'
        self.request.form['c10[]'] = 'Document'
        import ipdb; ipdb.set_trace()
