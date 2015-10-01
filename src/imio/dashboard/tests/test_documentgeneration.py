# -*- coding: utf-8 -*-

from DateTime import DateTime
from plone import api

from eea.facetednavigation.interfaces import ICriteria
from imio.dashboard.testing import IntegrationTestCase


class TestDocumentGeneration(IntegrationTestCase):
    """Test the document-generation that has been overrided from
       collective.documentgenerator to be 'dashboard aware'."""

    def setUp(self):
        """ """
        super(TestDocumentGeneration, self).setUp()
        # create a folder2 that will be displayed in the dashboard
        self.folder2 = api.content.create(id='folder2',
                                          type='Folder',
                                          title='Folder 2',
                                          container=self.portal)
        self.view = self.folder.restrictedTraverse('@@document-generation')
        self.helper = self.view.get_generation_context_helper()

    def test_get_generation_context(self):
        """
        Changes are about 'uids' and 'brains' that are added to the
        pod template generation context if possible
        if nothing particular is done, every elements of the displayed
        dashboard are added to the template generation context.
        """
        # order is respected so sort_on created
        # Date catalog queries are 1 minute sensitive...
        # make sure self.folder created is really older than self.folder2
        self.folder.setCreationDate(DateTime('2015/01/01 12:00'))
        self.folder.reindexObject()
        self.assertEquals(ICriteria(self.folder).get('c0').widget,
                          u'sorting')
        self.request.form['c0[]'] = 'created'

        gen_context = self.view._get_generation_context(self.helper)
        self.assertTrue('uids' in gen_context)
        self.assertEquals(len(gen_context['uids']), 2)
        self.assertTrue('brains' in gen_context)
        self.assertEquals(len(gen_context['brains']), 2)
        # brains are sorted according to uids list
        self.assertEquals(gen_context['uids'],
                          [brain.UID for brain in gen_context['brains']])

        # we have 2 elements in the dashboard : self.folder and self.folder2
        self.assertEquals(['Folder', 'Folder 2'],
                          [brain.Title for brain in gen_context['brains']])

        # order of query is kept in brains
        self.request.form['reversed'] = 'on'
        gen_context = self.view._get_generation_context(self.helper)
        self.assertEquals(['Folder 2', 'Folder'],
                          [brain.Title for brain in gen_context['brains']])

    def test_get_generation_context_filtered_query(self):
        """
        If a filter is used in the facetedQuery, elements displayed
        in the dashboard are correctly given to the template.
        """
        faceted_query = self.folder.restrictedTraverse('@@faceted_query')
        # for now 2 elements
        self.assertEquals(len(faceted_query.query()), 2)
        # filter on text, 'Folder 2'
        self.assertEquals(ICriteria(self.folder).get('c2').index,
                          u'SearchableText')
        self.request.form['c2[]'] = 'Folder 2'
        self.assertEquals(len(faceted_query.query()), 1)
        # generation context respect query
        gen_context = self.view._get_generation_context(self.helper)
        self.assertEquals(len(gen_context['uids']), 1)

        # facetedQuery is passed to the generation context as json
        # reset query, back to 2 elements found
        self.request.form = {}
        self.assertEquals(len(faceted_query.query()), 2)
        gen_context = self.view._get_generation_context(self.helper)
        self.assertEquals(len(gen_context['uids']), 2)
        # 'facetedQuery' is received as a serialized JSON of query criteria
        self.request.form['facetedQuery'] = '{"c2":"Folder 2"}'
        gen_context = self.view._get_generation_context(self.helper)
        self.assertEquals(len(gen_context['uids']), 1)

    def test_get_generation_context_filtered_uids(self):
        """We may also filter 'uids' directly if set in the REQUEST."""
        # for now 2 elements
        gen_context = self.view._get_generation_context(self.helper)
        self.assertEquals(len(gen_context['uids']), 2)
        self.assertEquals(len(gen_context['brains']), 2)
        self.request.form['uids'] = self.folder.UID()
        gen_context = self.view._get_generation_context(self.helper)
        self.assertEquals(len(gen_context['uids']), 1)
        self.assertEquals(len(gen_context['brains']), 1)
