# -*- coding: utf-8 -*-
import json

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.collection.interfaces import ICollection
from eea.facetednavigation.interfaces import IFacetedNavigable

from collective.documentgenerator.browser.generation_view import DocumentGenerationView
from collective.documentgenerator.content.pod_template import IPODTemplate
from collective.documentgenerator.viewlets.generationlinks import DocumentGeneratorLinksViewlet
from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget
from collective.eeafaceted.z3ctable.browser.views import FacetedTableView

from imio.dashboard.content.pod_template import IDashboardPODTemplate


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

    def get_generation_context(self, helper_view):
        """ """
        uids = self.request.get('uids', '')
        facetedQuery = self.request.get('facetedQuery', None)
        generation_context = {}
        brains = []
        # if we did not receive itemUids, generate it, it is necessary for printing methods
        if not uids and IFacetedNavigable.providedBy(self.context):
            faceted_query = self.context.restrictedTraverse('@@faceted_query')
            # maybe we have a facetedQuery? aka the meeting view was filtered and we want to print this result
            if facetedQuery:
                # put the facetedQuery criteria into the REQUEST.form
                for k, v in json.JSONDecoder().decode(facetedQuery).items():
                    # we receive list of elements, if we have only one elements, remove it from the list
                    if len(v) == 1:
                        v = v[0]
                    self.request.form[k] = v
            brains = faceted_query.query(batch=False)
            uids = [brain.UID for brain in brains]
        else:
            uids = uids.split(',')
        generation_context['uids'] = uids

        # if we have uids, let 'brains' be directly available in the template context too
        # brains could already fetched, if it is the case, use it, get it otherwise
        if not brains:
            catalog = getToolByName(self.context, 'portal_catalog')
            brains = catalog(UID=uids)

            # we need to sort found brains according to uids
            def getKey(item):
                return uids.index(item.UID)
            brains = sorted(brains, key=getKey)

        generation_context['brains'] = brains
        generation_context.update(super(IDDocumentGenerationView, self).get_generation_context(helper_view))
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
            object_provides=IDashboardPODTemplate.__identifier__
        )
        pod_templates = [self.context.unrestrictedTraverse(brain.getPath()) for brain in brains]

        return pod_templates
