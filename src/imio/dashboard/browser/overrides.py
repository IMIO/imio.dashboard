# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.collection.interfaces import ICollection
from eea.facetednavigation.browser.app.query import FacetedQueryHandler
from eea.facetednavigation.interfaces import IFacetedNavigable

from collective.documentgenerator.browser.generation_view import DocumentGenerationView
from collective.documentgenerator.content.pod_template import IPODTemplate
from collective.documentgenerator.viewlets.generationlinks import DocumentGeneratorLinksViewlet
from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget
from collective.eeafaceted.z3ctable.browser.views import FacetedTableView

from imio.dashboard.config import COMBINED_INDEX_PREFIX
from imio.dashboard.content.pod_template import IDashboardPODTemplate
from imio.dashboard.utils import getDashboardQueryResult


class IDFacetedTableView(FacetedTableView):

    def __init__(self, context, request):
        super(IDFacetedTableView, self).__init__(context, request)
        self.collection = self._set_collection()

    def _set_collection(self):
        if ICollection.providedBy(self.context):
            return self.context
        else:
            # if we can get the collection we are working with,
            # use customViewFields defined on it if any
            for criterion in self.criteria.values():
                if criterion.widget == CollectionWidget.widget_type:
                    # value is stored in the request with ending [], like 'c4[]'
                    collectionUID = self.request.get('{0}[]'.format(criterion.getId()))
                    if not collectionUID:
                        continue
                    catalog = getToolByName(self.context, 'portal_catalog')
                    collection = catalog(UID=collectionUID)
                    if collection:
                        return collection[0].getObject()

    def _getViewFields(self):
        """Returns fields we want to show in the table."""

        # if the context is a collection, get customViewFields on it
        if self.collection:
            return self.collection.getCustomViewFields()

        # else get default column names
        return super(IDFacetedTableView, self)._getViewFields()

    def orderColumns(self):
        """ Order columns of the table."""
        # do this to keep the column ordered as found on the field
        # 'customViewFields' of the collection if there is any
        if self.collection:
            for i, column in enumerate(self.columns):
                column.weight = i

        super(IDFacetedTableView, self).orderColumns()


class IDDocumentGenerationView(DocumentGenerationView):
    """Override the 'get_generation_context' propertly so 'get_base_generation_context'
       is available for sub-packages that want to extend the template generation context."""

    def _get_generation_context(self, helper_view):
        """ """
        generation_context = {'brains': [],
                              'uids': []}

        if IFacetedNavigable.providedBy(self.context):
            brains = getDashboardQueryResult(self.context)
            generation_context['brains'] = brains
            generation_context['uids'] = [brain.UID for brain in brains]

        generation_context.update(super(IDDocumentGenerationView, self)._get_generation_context(helper_view))
        return generation_context


class IDDocumentGeneratorLinksViewlet(DocumentGeneratorLinksViewlet):
    """Make the viewlet aware of the 'select box' column displayed
       using collective.eeafaceted.z3ctable in a eea.facetednavigation.
       For displaying out of dashboard."""

    render = ViewPageTemplateFile('templates/generationlinks.pt')

    def available(self):
        """
        Exclude this viewlet from faceted contexts.
        """
        available = super(IDDocumentGeneratorLinksViewlet, self).available()
        no_faceted_context = not bool(IFacetedNavigable.providedBy(self.context))
        return no_faceted_context and available

    def get_all_pod_templates(self):
        """
        Override to only return NOT dashboard templates.
        """
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog.unrestrictedSearchResults(
            object_provides={'query': IPODTemplate.__identifier__,
                             'not': IDashboardPODTemplate.__identifier__},
            sort_on='getObjPositionInParent'
        )
        pod_templates = [self.context.unrestrictedTraverse(brain.getPath()) for brain in brains]

        return pod_templates


class IDDashboardDocumentGeneratorLinksViewlet(DocumentGeneratorLinksViewlet):
    """For displaying on dashboards."""

    render = ViewPageTemplateFile('templates/generationlinks.pt')

    def available(self):
        """
        This viewlet is only visible on faceted contexts.
        """
        available = super(IDDashboardDocumentGeneratorLinksViewlet, self).available()
        faceted_context = bool(IFacetedNavigable.providedBy(self.context))
        return faceted_context and available

    def get_all_pod_templates(self):
        """
        Override to only return dashboard templates.
        """
        catalog = api.portal.get_tool(name='portal_catalog')
        brains = catalog.unrestrictedSearchResults(
            object_provides=IDashboardPODTemplate.__identifier__,
            sort_on='getObjPositionInParent'
        )
        pod_templates = [self.context.unrestrictedTraverse(brain.getPath()) for brain in brains]

        return pod_templates


class CombinedFacetedQueryHandler(FacetedQueryHandler):

    def criteria(self, sort=False, **kwargs):
        """Call original and triturate query to handle 'combined__' prefixed indexes."""
        criteria = super(CombinedFacetedQueryHandler, self).criteria(sort=sort, **kwargs)
        # if we have both real existing index and the 'combined__' prefixed one, combinate it
        res = {}
        for key, value in criteria:
            real_index = key.replace(COMBINED_INDEX_PREFIX, '')
            if key.startswith(COMBINED_INDEX_PREFIX) and real_index in criteria:
                # combine values to real index
                continue
            elif not key.startswith(COMBINED_INDEX_PREFIX):
                res[key] = value
        return res
