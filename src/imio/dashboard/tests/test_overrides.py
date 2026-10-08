# -*- coding: utf-8 -*-
from collective.eeafaceted.collectionwidget.interfaces import ICollectionCategories
from collective.eeafaceted.collectionwidget.utils import getCollectionLinkCriterion
from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget
from imio.dashboard.browser.overrides import IDRenderCategoryView
from imio.dashboard.interfaces import IContactsDashboard
from imio.dashboard.testing import IntegrationTestCase
from imio.helpers.catalog import addOrUpdateIndexes
from plone import api
from plone.app.testing import login
from plone.app.testing import TEST_USER_NAME
from zope.interface import alsoProvides

import lxml.html
import os


class TestIDRenderCategoryView(IntegrationTestCase):
    """Test the category rendering of the contacts dashboards."""

    def setUp(self):
        super(TestIDRenderCategoryView, self).setUp()
        self.contacts = api.content.create(container=self.portal, type='Folder', id='contacts', title='Contacts')
        self.orgs = self._category('orgs-searches', u'Organizations')
        self.widget = CollectionWidget(self.folder, self.request, getCollectionLinkCriterion(self.folder))

    def _category(self, cat_id, rights):
        category = api.content.create(container=self.contacts, type='Folder', id=cat_id, title=cat_id,
                                      rights=rights)
        alsoProvides(category, ICollectionCategories, IContactsDashboard)
        return category

    def _render(self, category):
        html = category.unrestrictedTraverse('@@render_collection_widget_category')(widget=self.widget)
        return lxml.html.fromstring(u'<div>{0}</div>'.format(html))

    def test__get_category_template(self):
        view = IDRenderCategoryView(self.orgs, self.request)
        self.assertTrue(view._get_category_template().filename.endswith('category_contact.pt'))
        # not a contacts dashboard
        self.assertIsNone(IDRenderCategoryView(self.folder, self.request)._get_category_template())
        # contact actions disabled
        view.manage_add_contact_actions = False
        self.assertIsNone(view._get_category_template())

    def test_call(self):
        portal_url = self.portal.absolute_url()
        view = self.orgs.unrestrictedTraverse('@@render_collection_widget_category')
        self.assertIsInstance(view, IDRenderCategoryView)
        # organizations category: add link opened in an overlay
        tree = self._render(self.orgs)
        link = tree.xpath('//div[@class="portlet_add_icons"]/a')[0]
        self.assertEqual(link.get('href'), portal_url + '/contacts/++add++organization')
        self.assertEqual(link.get('class'), 'add_contact_overlay')
        img = link.xpath('img')[0]
        self.assertEqual(img.get('src'), portal_url + '/organization_icon.png')
        self.assertEqual(img.get('title'), 'create_organization')
        self.assertEqual(tree.xpath('//div[@class="title"]')[0].text, 'Organizations')
        # contact lists category: no overlay class
        link = self._render(self._category('cls-searches', u'Contact lists')).xpath('//a')[0]
        self.assertEqual(link.get('href'), portal_url + '/contacts/contact-lists-folder')
        self.assertEqual(link.get('class'), '')
        self.assertEqual(link.xpath('img')[0].get('src'), portal_url + '/directory_icon.png')
        # unknown category: title only
        tree = self._render(self._category('other-searches', u'Other'))
        self.assertEqual(tree.xpath('//div[@class="portlet_add_icons"]'), [])
        self.assertEqual(tree.xpath('//div[@class="title"]')[0].text, 'Other')
        # a member that can not add content in contacts does not get the add link
        api.user.create(email='member@example.com', username='member', password='secret123', roles=('Member', ))
        login(self.portal, 'member')
        tree = self._render(self.orgs)
        self.assertEqual(tree.xpath('//div[@class="portlet_add_icons"]/a'), [])
        self.assertEqual(tree.xpath('//div[@class="title"]')[0].text, 'Organizations')
        login(self.portal, TEST_USER_NAME)


class TestCombinedFacetedQueryHandler(IntegrationTestCase):
    """Test the faceted_query override handling the 'combined__' indexes."""

    def test_criteria(self):
        addOrUpdateIndexes(self.portal, {'contained_types_and_states': ('KeywordIndex', {})})
        xmlpath = os.path.join(os.path.dirname(__file__), 'faceted_conf', 'combined_index_widgets.xml')
        with open(xmlpath) as xml_file:
            self.folder.unrestrictedTraverse('@@faceted_exportimport').import_xml(import_file=xml_file)
        faceted_query = self.folder.restrictedTraverse('@@faceted_query')
        # combined indexes are removed from 'facet.field'
        criteria = faceted_query.criteria()
        self.assertIn('contained_types_and_states', criteria['facet.field'])
        self.assertNotIn('combined__contained_types_and_states', criteria['facet.field'])
        # only the combined index: used as the real index
        self.request.form['c11[]'] = 'private'
        criteria = faceted_query.criteria()
        self.assertEqual(criteria['contained_types_and_states']['query'], 'private')
        # the combined key is kept too
        self.assertEqual(criteria['combined__contained_types_and_states']['query'], 'private')
        # both indexes, scalar values
        self.request.form['c10[]'] = 'Document'
        criteria = faceted_query.criteria()
        self.assertEqual(criteria['contained_types_and_states']['query'], ['Document__private'])
        self.assertNotIn('combined__contained_types_and_states', criteria)
        # both indexes, list values
        self.request.form['c10[]'] = ['Document', 'Folder']
        self.request.form['c11[]'] = ['private', 'published']
        self.assertEqual(faceted_query.criteria()['contained_types_and_states']['query'],
                         ['Document__private', 'Folder__private', 'Document__published', 'Folder__published'])
