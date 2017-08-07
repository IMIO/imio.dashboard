# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.collection.interfaces import ICollection
from eea.facetednavigation.browser.app.query import FacetedQueryHandler
from eea.facetednavigation.interfaces import IFacetedNavigable

from collective.documentgenerator.browser.generation_view import DocumentGenerationView
from collective.documentgenerator.viewlets.generationlinks import DocumentGeneratorLinksViewlet
from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget
from collective.eeafaceted.z3ctable.browser.views import FacetedTableView

from imio.dashboard.config import COMBINED_INDEX_PREFIX
from imio.dashboard.content.pod_template import IDashboardPODTemplate
from imio.dashboard.utils import getDashboardQueryResult


class IDFacetedTableView(FacetedTableView):

    ignoreColumnWeight = True

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


class IDDocumentGenerationView(DocumentGenerationView):
    """Override the 'get_generation_context' properly so 'get_base_generation_context'
       is available for sub-packages that want to extend the template generation context."""

    def _get_generation_context(self, helper_view, pod_template):
        """ """
        # if we are in base viewlet (not dashboard), return the base context
        if 'facetedQuery' not in self.request.form:
            return super(IDDocumentGenerationView, self)._get_generation_context(helper_view, pod_template)

        generation_context = {'brains': [],
                              'uids': []}

        if IFacetedNavigable.providedBy(self.context):
            brains = getDashboardQueryResult(self.context)
            generation_context['brains'] = brains
            if getattr(pod_template, 'use_objects', False):
                wrapped_objects = []
                brain_and_objects = []
                for brain in brains:
                    generation_context['uids'].append(brain.UID)
                    obj = brain.getObject()
                    helper = obj.unrestrictedTraverse('@@document_generation_helper_view')
                    wrapped_objects.append((helper.context, helper))
                    brain_and_objects.append((brain, helper.context, helper))
                generation_context['objects'] = wrapped_objects
                generation_context['all'] = brain_and_objects
            else:
                generation_context['uids'] = [brain.UID for brain in brains]

        generation_context.update(super(IDDocumentGenerationView, self)._get_generation_context(helper_view,
                                                                                                pod_template))
        return generation_context


class IDDashboardDocumentGeneratorLinksViewlet(DocumentGeneratorLinksViewlet):
    """For displaying on dashboards."""

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
        res = criteria.copy()
        for key, value in criteria.items():
            # bypass if it is not a 'combined' index
            if not key.startswith(COMBINED_INDEX_PREFIX):
                continue

            real_index = key.replace(COMBINED_INDEX_PREFIX, '')
            # if we have both real existing index and the 'combined__' prefixed one, combinate it
            if real_index in criteria:
                # combine values to real index
                real_index_values = criteria[real_index]['query']
                if not hasattr(real_index_values, '__iter__'):
                    real_index_values = [real_index_values]
                combined_index_values = criteria[key]['query']
                if not hasattr(combined_index_values, '__iter__'):
                    combined_index_values = [combined_index_values]
                combined_values = []
                for value in combined_index_values:
                    for real_index_value in real_index_values:
                        combined_values.append(real_index_value + '__' + value)
                # update real_index and pop current key
                res[real_index]['query'] = combined_values
                res.pop(key)
            # if we have only the 'combined__' prefixed one, use it as real index
            elif real_index not in criteria:
                res[real_index] = value
        return res
