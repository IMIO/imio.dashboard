# -*- coding: utf-8 -*-
import logging
from os import path
from zope.interface import noLongerProvides

from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget

from eea.facetednavigation.criteria.interfaces import ICriteria
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable
from eea.facetednavigation.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.layout.interfaces import IFacetedLayout

from imio.dashboard.config import NO_FACETED_EXCEPTION_MSG

logger = logging.getLogger('imio.dashboard: utils')


class NoFacetedViewDefinedException(Exception):
    """ To be raised when a context has no faceted view defined on it. """


def getCollectionLinkCriterion(faceted_context):
    """Return the CollectionLink criterion instance of a
       context with a faceted navigation/search view on it."""
    if not IFacetedNavigable.providedBy(faceted_context):
        raise NoFacetedViewDefinedException(NO_FACETED_EXCEPTION_MSG)

    criteria = ICriteria(faceted_context).criteria
    for criterion in criteria:
        if criterion.widget == CollectionWidget.widget_type:
            return criterion


def enableFacetedDashboardFor(obj, xmlpath=None):
    """Enable a faceted view on obj and import a
       specific xml if given p_xmlpath."""
    # already a faceted?
    if IFacetedNavigable.providedBy(obj):
        logger.error("Faceted navigation is already enabled for '%s'" %
                     '/'.join(obj.getPhysicalPath()))
        return

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
    if xmlpath is not None:
        if path.exists(xmlpath):
            obj.unrestrictedTraverse('@@faceted_exportimport').import_xml(
                import_file=open(xmlpath))
        else:
            logger.error("Specified xml file '%s' doesn't exist" % xmlpath)
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
