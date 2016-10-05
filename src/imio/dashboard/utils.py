# -*- coding: utf-8 -*-
import json
from os import path
from zope.interface import noLongerProvides

from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget

from eea.facetednavigation.criteria.interfaces import ICriteria
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from eea.facetednavigation.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.layout.interfaces import IFacetedLayout

from imio.dashboard.config import NO_FACETED_EXCEPTION_MSG
from imio.dashboard.config import NO_COLLECTIONWIDGET_EXCEPTION_MSG
from imio.dashboard.interfaces import NoCollectionWidgetDefinedException
from imio.dashboard.interfaces import NoFacetedViewDefinedException

from plone import api

import logging
logger = logging.getLogger('imio.dashboard: utils')


def _get_criterion(faceted_context, criterion_type):
    """Return the given criterion_type instance of a
       context with a faceted navigation/search view on it."""
    if not IFacetedNavigable.providedBy(faceted_context):
        raise NoFacetedViewDefinedException(NO_FACETED_EXCEPTION_MSG)

    criteria = ICriteria(faceted_context).criteria
    for criterion in criteria:
        if criterion.widget == criterion_type:
            return criterion


def getCollectionLinkCriterion(faceted_context):
    """Return the CollectionLink criterion used by faceted_context."""
    criterion = _get_criterion(faceted_context,
                               criterion_type=CollectionWidget.widget_type)
    if not criterion:
        raise NoCollectionWidgetDefinedException(NO_COLLECTIONWIDGET_EXCEPTION_MSG)

    return criterion


def getCurrentCollection(faceted_context):
    """Return the Collection currently used by the faceted :
       - first get the collection criterion;
       - then look in the request the used UID and get the corresponding Collection."""
    criterion = getCollectionLinkCriterion(faceted_context)
    collectionUID = faceted_context.REQUEST.form.get('{0}[]'.format(criterion.__name__))
    # if not collectionUID, maybe we have a 'facetedQuery' in the REQUEST
    if not collectionUID and \
       ('facetedQuery' in faceted_context.REQUEST.form and faceted_context.REQUEST.form['facetedQuery']):
        query = json.loads(faceted_context.REQUEST.form['facetedQuery'])
        collectionUID = query.get(criterion.__name__)
    if collectionUID:
        catalog = api.portal.get_tool('portal_catalog')
        return catalog(UID=collectionUID)[0].getObject()


def enableFacetedDashboardFor(obj, xmlpath=None):
    """Enable a faceted view on obj and import a
       specific xml if given p_xmlpath."""
    # already a faceted?
    if IFacetedNavigable.providedBy(obj):
        logger.error("Faceted navigation is already enabled for '%s'" %
                     '/'.join(obj.getPhysicalPath()))
        return

    # do not go further if xmlpath does not exist
    if xmlpath and not path.exists(xmlpath):
        raise Exception("Specified xml file '%s' doesn't exist" % xmlpath)
    # .enable() here under will redirect to enabled faceted
    # we cancel this, safe previous RESPONSE status and location
    response_status = obj.REQUEST.RESPONSE.getStatus()
    response_location = obj.REQUEST.RESPONSE.getHeader('location')
    obj.unrestrictedTraverse('@@faceted_subtyper').enable()

    # use correct layout in the faceted
    IFacetedLayout(obj).update_layout('faceted-table-items')
    # show the left portlets
    if IHidePloneLeftColumn.providedBy(obj):
        noLongerProvides(obj, IHidePloneLeftColumn)
    # import configuration
    if xmlpath:
        obj.unrestrictedTraverse('@@faceted_exportimport').import_xml(
            import_file=open(xmlpath))
    obj.reindexObject()
    obj.REQUEST.RESPONSE.status = response_status
    obj.REQUEST.RESPONSE.setHeader('location', response_location or '')


def _updateDefaultCollectionFor(folderObj, default_uid):
    """Use p_default_uid as the default collection selected
       for the CollectionWidget used on p_folderObj."""
    # folder should be a facetednav
    if not IFacetedNavigable.providedBy(folderObj):
        raise NoFacetedViewDefinedException(NO_FACETED_EXCEPTION_MSG)

    criterion = getCollectionLinkCriterion(folderObj)
    criterion.default = default_uid
    # make change persist!
    ICriteria(folderObj).criteria._p_changed = True


def getDashboardQueryResult(faceted_context):
    """
    Return dashboard selelected items of a faceted query.
    """
    if not IFacetedNavigable.providedBy(faceted_context):
        raise NoFacetedViewDefinedException(NO_FACETED_EXCEPTION_MSG)

    request = faceted_context.REQUEST
    uids = request.form.get('uids', '')
    faceted_query = request.form.get('facetedQuery', None)

    brains = []
    # maybe we have a facetedQuery? aka the meeting view was filtered and we want to print this result
    if not uids:
        if faceted_query:
            # put the facetedQuery criteria into the REQUEST.form
            for k, v in json.JSONDecoder().decode(faceted_query).items():
                # we receive list of elements, if we have only one elements, remove it from the list
                if isinstance(v, list) and len(v) == 1:
                    v = v[0]
                request.form['{0}[]'.format(k)] = v
        faceted = faceted_context.restrictedTraverse('@@faceted_query')
        brains = faceted.query(batch=False)
    # if we have uids, let 'brains' be directly available in the template context too
    # brains could already fetched, if it is the case, use it, get it otherwise
    elif uids:
        uids = uids.split(',')
        catalog = api.portal.get_tool('portal_catalog')
        brains = catalog(UID=uids)

        # we need to sort found brains according to uids
        def getKey(item):
            return uids.index(item.UID)
        brains = sorted(brains, key=getKey)
    return brains


def _get_criterion_by_attr(faceted_context, attr_name, value_to_match):
    """
    """
    if not IFacetedNavigable.providedBy(faceted_context):
        raise NoFacetedViewDefinedException(NO_FACETED_EXCEPTION_MSG)

    criterions = ICriteria(faceted_context)
    for criterion in criterions.values():
        if not hasattr(criterion, attr_name):
            continue
        else:
            attr = getattr(criterion, attr_name)
            value = hasattr(attr, '__call__') and attr() or attr
            if value == value_to_match:
                return criterion


def getCriterionByTitle(faceted_context, title):
    """
    Return criterion with title 'title'.
    """
    return _get_criterion_by_attr(faceted_context, 'title', title)


def getCriterionByIndex(faceted_context, index):
    """
    Return criterion with index named 'index'.
    """
    return _get_criterion_by_attr(faceted_context, 'index', index)
