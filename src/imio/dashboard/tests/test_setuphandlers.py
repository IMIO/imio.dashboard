# -*- coding: utf-8 -*-
from collective.eeafaceted.collectionwidget.interfaces import ICollectionCategories
from collective.eeafaceted.collectionwidget.utils import getCollectionLinkCriterion
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from imio.dashboard.interfaces import IContactsDashboard
from imio.dashboard.setuphandlers import _add_db_col_folder
from imio.dashboard.setuphandlers import _createDashboardCollections
from imio.dashboard.setuphandlers import add_orgs_searches
from imio.dashboard.testing import IntegrationTestCase
from plone import api
from plone.dexterity.fti import DexterityFTI


class TestSetuphandlers(IntegrationTestCase):
    """Test the contacts searches setup helpers."""

    def setUp(self):
        super(TestSetuphandlers, self).setUp()
        self.contacts = api.content.create(container=self.portal, type='Folder', id='contacts', title='Contacts')

    def test__add_db_col_folder(self):
        col_folder = _add_db_col_folder(self.contacts, 'orgs-searches', 'Organizations searches', 'Organizations',
                                        markers=[IContactsDashboard])
        self.assertEqual(col_folder.Title(), 'Organizations searches')
        self.assertEqual(col_folder.Rights(), 'Organizations')
        self.assertEqual(col_folder.getConstrainTypesMode(), 1)
        self.assertEqual(col_folder.getLocallyAllowedTypes(), ('DashboardCollection', ))
        self.assertEqual(col_folder.getImmediatelyAddableTypes(), ('DashboardCollection', ))
        self.assertTrue(ICollectionCategories.providedBy(col_folder))
        self.assertTrue(IContactsDashboard.providedBy(col_folder))
        # existing folder returned untouched
        self.assertEqual(_add_db_col_folder(self.contacts, 'orgs-searches', 'Other'), col_folder)
        self.assertEqual(col_folder.Title(), 'Organizations searches')
        # no marker
        other = _add_db_col_folder(self.contacts, 'other', 'Other')
        self.assertTrue(ICollectionCategories.providedBy(other))
        self.assertFalse(IContactsDashboard.providedBy(other))

    def test__createDashboardCollections(self):
        query = [{'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.is', 'v': ['Folder']}]
        collections = [
            {'id': 'all', 'tit': u'All', 'subj': (u'search', ), 'query': query, 'cond': u'', 'bypass': [],
             'flds': (u'select_row', u'pretty_link', u'actions'), 'sort': u'sortable_title', 'rev': False,
             'count': False},
            {'id': ''},
            {'id': 'second', 'tit': u'Second', 'query': query, 'cond': u'python: True', 'bypass': ['Manager'],
             'flds': (u'pretty_link', ), 'sort': u'created', 'rev': True, 'count': True},
        ]
        _createDashboardCollections(self.contacts, collections)
        self.assertEqual(self.contacts.objectIds(), ['all', 'second'])
        dc = self.contacts['all']
        self.assertEqual(dc.portal_type, 'DashboardCollection')
        self.assertEqual(dc.Title(), 'All')
        self.assertEqual(dc.query, query)
        self.assertEqual(dc.customViewFields, (u'select_row', u'pretty_link', u'actions'))
        self.assertEqual(dc.sort_on, u'sortable_title')
        self.assertFalse(dc.sort_reversed)
        self.assertFalse(dc.showNumberOfItems)
        self.assertEqual(dc.b_size, 30)
        self.assertEqual(dc.limit, 0)
        self.assertEqual(dc.Subject(), ('search', ))
        self.assertEqual(api.content.find(UID=dc.UID(), Subject='search')[0].getObject(), dc)
        self.assertEqual(dc.getLayout(), 'tabular_view')
        dc2 = self.contacts['second']
        self.assertEqual(dc2.tal_condition, u'python: True')
        self.assertEqual(dc2.roles_bypassing_talcondition, ['Manager'])
        self.assertTrue(dc2.sort_reversed)
        self.assertTrue(dc2.showNumberOfItems)
        self.assertEqual(dc2.Subject(), ())
        # existing collections are kept and moved to their position
        dc.setTitle(u'Changed')
        _createDashboardCollections(self.contacts, [collections[2], collections[0]])
        self.assertEqual(self.contacts.objectIds(), ['second', 'all'])
        self.assertEqual(dc.Title(), 'Changed')

    def test_add_orgs_searches(self):
        # the collective.contact.core 'directory' type is faked
        self.portal.portal_types._setObject('directory', DexterityFTI('directory'))
        self.portal.portal_types.directory.filter_content_types = True
        api.content.create(container=self.contacts, type='Document', id='doc', title='Document')
        add_orgs_searches(self.portal, add_contact_lists_collections=False)
        self.assertEqual(self.contacts.objectIds(), ['orgs-searches', 'hps-searches', 'persons-searches', 'doc'])
        self.assertTrue(self.portal.portal_types.directory.filter_content_types)
        expected = {'orgs-searches': ('Organizations searches', 'Organizations', 'all_orgs', 'organization'),
                    'hps-searches': ('Held positions searches', 'Held positions', 'all_hps', 'held_position'),
                    'persons-searches': ('Persons searches', 'Persons', 'all_persons', 'person')}
        for cat_id, (title, rights, dc_id, portal_type) in expected.items():
            category = self.contacts[cat_id]
            self.assertEqual((category.Title(), category.Rights()), (title, rights))
            self.assertTrue(IContactsDashboard.providedBy(category))
            self.assertTrue(IFacetedNavigable.providedBy(category))
            self.assertEqual(category.objectIds(), [dc_id])
            self.assertEqual(category[dc_id].Title(), dc_id)
            self.assertEqual(category[dc_id].query[0]['v'], [portal_type])
            self.assertEqual(getCollectionLinkCriterion(category).default, category[dc_id].UID())
            self.assertTrue(len(ICriteria(category).keys()) > 1)
        # contacts is a faceted dashboard showing the organizations by default
        self.assertTrue(IFacetedNavigable.providedBy(self.contacts))
        self.assertEqual(getCollectionLinkCriterion(self.contacts).default,
                         self.contacts['orgs-searches']['all_orgs'].UID())
        # known issue: contact-lists-searches.xml has an empty int 'maxitems' (see MIGRATION.md)
        self.assertRaises(ValueError, add_orgs_searches, self.portal)
