# -*- coding: utf-8 -*-
from eea.facetednavigation.criteria.interfaces import ICriteria
from eea.facetednavigation.interfaces import IFacetedNavigable
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.services import Service
from zope.component import getMultiAdapter, getUtility
from zope.interface import implements
from zope.publisher.interfaces import IPublishTraverse
from zope.schema.interfaces import IVocabularyFactory


class UserDashboardsGet(Service):
    implements(IPublishTraverse)

    def serializeVocabulary(self, context, vocabulary_name):
        if not vocabulary_name:
            return {}
        factory = getUtility(IVocabularyFactory, name=vocabulary_name)
        vocabulary = factory(context)
        serializer = getMultiAdapter(
            (vocabulary, self.request), interface=ISerializeToJson
        )
        return serializer(
            "{}/@vocabularies/{}".format(context.absolute_url(), vocabulary_name)
        )

    def reply(self):
        dashboards = {}
        catalog = api.portal.get_tool("portal_catalog")
        for brain in catalog(object_provides=IFacetedNavigable.__identifier__):
            dashboard = brain.getObject()
            dashboard_criteria = []
            for criteria in ICriteria(dashboard).criteria:
                vocabulary_values = self.serializeVocabulary(
                    dashboard, criteria.vocabulary
                )
                if vocabulary_values and not vocabulary_values["items"]:
                    vocabulary_values = {}
                criteria_hash = {
                    "title": criteria.title,
                    "id": criteria.getId(),
                    "vocabulary": criteria.vocabulary,
                    "default": criteria.default,
                    "values": vocabulary_values,
                }
                dashboard_criteria.append(criteria_hash)
            dashboards[dashboard.getId()] = {
                "title": dashboard.Title(),
                "path": dashboard.absolute_url(),
                "uid": dashboard.UID(),
                "criteria": dashboard_criteria,
            }
        return dashboards
