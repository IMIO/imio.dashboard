# -*- coding: utf-8 -*-
from collective.eeafaceted.collectionwidget.interfaces import ICollectionCategories
from collective.eeafaceted.dashboard.utils import enableFacetedDashboardFor
from imio.dashboard import logger
from imio.dashboard.interfaces import IContactsDashboard
from plone import api
from Products.CMFPlone.utils import base_hasattr
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.interface import alsoProvides

import os


def isNotCurrentProfile(context):
    return context.readDataFile("imiodashboard_marker.txt") is None


def post_install(context):
    """Post install script"""
    if isNotCurrentProfile(context):
        return


def _(msgid, domain='imio.dashboard'):
    translation_domain = queryUtility(ITranslationDomain, domain)
    sp = api.portal.get().portal_properties.site_properties
    return translation_domain.translate(msgid, target_language=sp.getProperty('default_language', 'fr'))


def _add_db_col_folder(folder, id, title, displayed='', markers=[]):
    if base_hasattr(folder, id):
        return folder[id]

    folder.invokeFactory('Folder', id=id, title=title, rights=displayed)
    col_folder = folder[id]
    col_folder.setConstrainTypesMode(1)
    col_folder.setLocallyAllowedTypes(['DashboardCollection'])
    col_folder.setImmediatelyAddableTypes(['DashboardCollection'])
    wfTool = api.portal.get_tool('portal_workflow')
    if "show_internally" in wfTool.getTransitionsFor(col_folder):
        wfTool.doActionFor(col_folder, "show_internally")
    alsoProvides(col_folder, ICollectionCategories)
    for marker in markers:
        alsoProvides(col_folder, marker)
    return col_folder


def _createOrganizationsCollections(folder):
    """ create some dashboard collections """
    collections = [
        {'id': 'all_orgs', 'tit': _('all_orgs'), 'subj': (u'search', ), 'query': [
            {'i': 'portal_type',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': ['organization']}],
            'cond': u"", 'bypass': [],
            'flds': (u'select_row', u'org_pretty_link_with_additional_infos',
                     u'SelectedInPlonegroupColumn', u'PloneGroupUsersGroupsColumn',
                     u'review_state', u'CreationDate', u'actions'),
            'sort': u'sortable_title', 'rev': False, 'count': False},
    ]
    _createDashboardCollections(folder, collections)


def _createHeldPositionsCollections(folder):
    """ create some dashboard collections """
    collections = [
        {'id': 'all_hps', 'tit': _('all_hps'), 'subj': (u'search', ), 'query': [
            {'i': 'portal_type',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': ['held_position']}],
            'cond': u"", 'bypass': [],
            'flds': (u'select_row', u'org_pretty_link_with_additional_infos',
                     u'review_state', u'CreationDate', u'actions'),
            'sort': u'sortable_title', 'rev': False, 'count': False},
    ]
    _createDashboardCollections(folder, collections)


def _createPersonsCollections(folder):
    """ create some dashboard collections """
    collections = [
        {'id': 'all_persons', 'tit': _('all_persons'), 'subj': (u'search', ), 'query': [
            {'i': 'portal_type',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': ['person']}],
            'cond': u"", 'bypass': [],
            'flds': (u'select_row', u'org_pretty_link_with_additional_infos',
                     u'review_state', u'CreationDate', u'actions'),
            'sort': u'sortable_title', 'rev': False, 'count': False},
    ]
    _createDashboardCollections(folder, collections)


def _createContactListsCollections(folder):
    """ create some dashboard collections """
    collections = [
        {'id': 'all_cls', 'tit': _('all_cls'), 'subj': (u'search', ), 'query': [
            {'i': 'portal_type',
             'o': 'plone.app.querystring.operation.selection.is',
             'v': ['contact_list']}],
            'cond': u"", 'bypass': [],
            'flds': (u'select_row', u'pretty_link', u'relative_path',
                     u'review_state', u'CreationDate', u'actions'),
            'sort': u'sortable_title', 'rev': False, 'count': False},
    ]
    _createDashboardCollections(folder, collections)


def _createDashboardCollections(folder, collections):
    """
        create some dashboard collections in searches folder
    """
    wfTool = api.portal.get_tool('portal_workflow')
    for i, dic in enumerate(collections):
        if not dic.get('id'):
            continue
        if not base_hasattr(folder, dic['id']):
            folder.invokeFactory("DashboardCollection",
                                 dic['id'],
                                 title=dic['tit'],
                                 query=dic['query'],
                                 tal_condition=dic['cond'],
                                 roles_bypassing_talcondition=dic['bypass'],
                                 customViewFields=dic['flds'],
                                 showNumberOfItems=dic['count'],
                                 sort_on=dic['sort'],
                                 sort_reversed=dic['rev'],
                                 b_size=30,
                                 limit=0)
            collection = folder[dic['id']]
            if "show_internally" in wfTool.getTransitionsFor(collection):
                wfTool.doActionFor(collection, "show_internally")
            if 'subj' in dic:
                collection.setSubject(dic['subj'])
                collection.reindexObject(['Subject'])
            collection.setLayout('tabular_view')
        if folder.getObjectPosition(dic['id']) != i:
            folder.moveObjectToPosition(dic['id'], i)


def add_orgs_searches(portal, add_contact_lists_collections=True):
    """ """
    # add organizations searches
    portal.portal_types.directory.filter_content_types = False
    contacts = portal.contacts
    col_folder = _add_db_col_folder(contacts,
                                    'orgs-searches',
                                    _("Organizations searches"),
                                    _("Organizations"),
                                    markers=[IContactsDashboard])
    contacts.moveObjectToPosition('orgs-searches', 0)
    _createOrganizationsCollections(col_folder)
    # createStateCollections(col_folder, 'organization')
    xml_base_path = os.path.dirname(__file__) + '/faceted_conf/'
    enableFacetedDashboardFor(col_folder, xmlpath=xml_base_path + 'organizations-searches.xml',
                              default_UID=col_folder['all_orgs'].UID())
    # configure contacts faceted
    enableFacetedDashboardFor(contacts, default_UID=col_folder['all_orgs'].UID())
    # add held positions searches
    col_folder = _add_db_col_folder(contacts,
                                    'hps-searches',
                                    _("Held positions searches"),
                                    _("Held positions"),
                                    markers=[IContactsDashboard])
    contacts.moveObjectToPosition('hps-searches', 1)
    _createHeldPositionsCollections(col_folder)
    # createStateCollections(col_folder, 'held_position')
    enableFacetedDashboardFor(col_folder, xmlpath=xml_base_path + 'held-positions-searches.xml',
                              default_UID=col_folder['all_hps'].UID())
    # add persons searches
    col_folder = _add_db_col_folder(contacts,
                                    'persons-searches',
                                    _("Persons searches"),
                                    _("Persons"),
                                    markers=[IContactsDashboard])
    contacts.moveObjectToPosition('persons-searches', 2)
    _createPersonsCollections(col_folder)
    # createStateCollections(col_folder, 'person')
    enableFacetedDashboardFor(col_folder, xmlpath=xml_base_path + 'persons-searches.xml',
                              default_UID=col_folder['all_persons'].UID())
    # add contact list searches
    if add_contact_lists_collections:
        col_folder = _add_db_col_folder(contacts,
                                        'cls-searches',
                                        _("Contact list searches"),
                                        _("Contact lists"),
                                        markers=[IContactsDashboard])
        contacts.moveObjectToPosition('cls-searches', 3)
        _createContactListsCollections(col_folder)
        # createStateCollections(col_folder, 'contact_list')
        enableFacetedDashboardFor(col_folder, xmlpath=xml_base_path + 'contact-lists-searches.xml',
                                  default_UID=col_folder['all_cls'].UID())

    portal.portal_types.directory.filter_content_types = True
    logger.info('Organizations searches created')
