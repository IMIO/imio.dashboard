# encoding: utf-8

from operator import attrgetter

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone import api
from plone.memoize import ram
from Products.CMFPlone.utils import safe_unicode

from collective.behavior.talcondition.interfaces import ITALConditionable
from collective.behavior.talcondition.utils import evaluateExpressionFor
from collective.eeafaceted.collectionwidget.vocabulary import CollectionVocabulary

from imio.dashboard.interfaces import IDashboardCollection

from Products.CMFCore.utils import getToolByName


class ConditionAwareCollectionVocabulary(CollectionVocabulary):
    def __call__(self, context, query=None):
        """Same behaviour as the original CollectionVocabulary
           but we will filter Collections regarding the defined tal_condition."""
        terms = super(ConditionAwareCollectionVocabulary, self).__call__(context, query=query)

        filtered_terms = []
        for term in terms:
            collection = term.value
            # if collection is ITALConditionable, evaluate the TAL condition
            # except if current user is Manager
            if ITALConditionable.providedBy(collection):
                if not evaluateExpressionFor(collection):
                    continue
            filtered_terms.append(term)
        return SimpleVocabulary(filtered_terms)

ConditionAwareCollectionVocabularyFactory = ConditionAwareCollectionVocabulary()


class CreatorsVocabulary(object):
    implements(IVocabularyFactory)

    def __call__cachekey(method, self, context):
        '''cachekey method for self.__call__.'''
        catalog = getToolByName(context, 'portal_catalog')
        return context, catalog.uniqueValuesFor('Creator')

    def _get_user_fullname(self, login):
        """Get fullname without using getMemberInfo that is slow slow slow..."""
        storage = api.portal.get_tool('acl_users').mutable_properties._storage
        data = storage.get(login, None)
        if data is not None:
            return data.get('fullname', '') or login
        else:
            return login

    @ram.cache(__call__cachekey)
    def __call__(self, context):
        """ """
        catalog = getToolByName(context, 'portal_catalog')
        res = []
        for creator in catalog.uniqueValuesFor('Creator'):
            fullname = self._get_user_fullname(creator)
            res.append(SimpleTerm(creator,
                                  creator,
                                  safe_unicode(fullname))
                       )
        res = sorted(res, key=attrgetter('title'))
        return SimpleVocabulary(res)

CreatorsVocabularyFactory = CreatorsVocabulary()


class DashboardCollectionsVocabulary(object):
    """
    Vocabulary factory for 'dashboard_collections' field of DashboardPODTemplate.
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        catalog = api.portal.get_tool('portal_catalog')
        collection_brains = catalog(object_provides=IDashboardCollection.__identifier__)
        vocabulary = SimpleVocabulary(
            [SimpleTerm(b.UID, b.UID, b.Title) for b in collection_brains]
        )
        return vocabulary

DashboardCollectionsVocabularyFactory = DashboardCollectionsVocabulary()
