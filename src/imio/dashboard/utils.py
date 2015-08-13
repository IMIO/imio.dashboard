# -*- coding: utf-8 -*-

from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget

from eea.facetednavigation.criteria.interfaces import ICriteria
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable

from imio.dashboard.interfaces import NoFacetedViewDefinedException


def _updateDefaultCollectionFor(folderObj, default_uid):
    """Use p_default_uid as the default collection selected
        for the CollectionWidget used on p_folderObj."""
    # folder should be a facetednav
    if not IFacetedNavigable.providedBy(folderObj):
        return NoFacetedViewDefinedException

    criteria = ICriteria(folderObj).criteria
    for criterion in criteria:
        if criterion.widget == CollectionWidget.widget_type:
            criterion.default = default_uid


def getCollectionLinkCriterion(faceted_context):
    """
    Return the CollectionLink criterion instance of a context with a
    faceted navigation/search view on it.
    """
    if not IFacetedNavigable.providedBy(faceted_context):
        return NoFacetedViewDefinedException

    criteria = ICriteria(faceted_context).criteria
    for criterion in criteria:
        if criterion.widget == CollectionWidget.widget_type:
            return criterion


def getCollectionLinkWidget(faceted_context):
    """
    Return the CollectionLink widget instance of a context with a
    faceted navigation/search view on it.
    """
    criterion = getCollectionLinkCriterion(faceted_context)
    return criterion.widget
