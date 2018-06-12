# encoding: utf-8

from operator import attrgetter

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone import api
from plone.memoize import ram
from Products.CMFPlone.utils import safe_unicode
from collective.eeafaceted.collectionwidget.vocabulary import CollectionVocabulary
from eea.facetednavigation.interfaces import IFacetedNavigable
from eea.faceted.vocabularies.catalog import CatalogIndexesVocabulary

from imio.dashboard.config import COMBINED_INDEX_PREFIX
from imio.helpers.cache import get_cachekey_volatile


class CachedCollectionVocabulary(CollectionVocabulary):

    def __call___cachekey(method, self, context):
        '''cachekey method for self.__call__.'''
        return self._cache_invalidation_key(context)

    def _cache_invalidation_key(self, context):
        '''The key will rely on :
           - current user, in case faceted is stored in the user personal folder;
           - a stored cache volatile that is destroyed if a DashboardCollection is modified somewhere;
           - the first facetednavigable context encountered when ascending context parents.'''
        user = api.user.get_current()
        date = get_cachekey_volatile('collective.eeafaceted.dashboard.conditionawarecollectionvocabulary')
        parent = context
        while not IFacetedNavigable.providedBy(parent) and parent.meta_type != 'Plone Site':
            parent = parent.aq_parent
        return user, date, parent

    @ram.cache(__call___cachekey)
    def __call__(self, context):
        """Same behaviour as the original CollectionVocabulary, just cached."""
        terms = super(CachedCollectionVocabulary, self).__call__(context)
        return terms


CachedCollectionVocabularyFactory = CachedCollectionVocabulary()


class CreatorsVocabulary(object):
    implements(IVocabularyFactory)

    def __call__cachekey(method, self, context):
        '''cachekey method for self.__call__.'''
        catalog = api.portal.get_tool('portal_catalog')
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
        catalog = api.portal.get_tool('portal_catalog')
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


class CombinedCatalogIndexesVocabulary(CatalogIndexesVocabulary):
    """ Return catalog indexes as vocabulary and dummy indexes prefixed
        with 'combined__' used to be combined at query time with the corresponding
        index not prefixed with 'combined__'.
    """

    def __call__(self, context):
        """ Call original indexes and append 'combined__' prefixed ones.
        """
        indexes = super(CombinedCatalogIndexesVocabulary, self).__call__(context)
        res = list(indexes)
        for index in indexes:
            if not index.value:
                # ignore the '' value
                continue
            key = COMBINED_INDEX_PREFIX + index.value
            value = '(Combined) ' + index.title
            res.append(SimpleTerm(key, key, value))
        return SimpleVocabulary(res)
