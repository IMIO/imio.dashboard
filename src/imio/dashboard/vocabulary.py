# encoding: utf-8

from eea.faceted.vocabularies.catalog import CatalogIndexesVocabulary
from imio.dashboard import ImioDashboardMessageFactory as _
from imio.dashboard.config import COMBINED_INDEX_PREFIX
from imio.helpers.content import get_user_fullname
from operator import attrgetter
from plone import api
from plone.memoize import ram
from Products.CMFPlone.utils import safe_unicode
from zope.i18n import translate
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


HAS_PLONEGROUP = True
try:
    from collective.contact.plonegroup.interfaces import INotPloneGroupContact
    from collective.contact.plonegroup.interfaces import IPloneGroupContact
except ImportError:
    HAS_PLONEGROUP = False


@implementer(IVocabularyFactory)
class CreatorsVocabulary(object):

    def __call__cachekey(method, self, context):
        '''cachekey method for self.__call__.'''
        catalog = api.portal.get_tool('portal_catalog')
        return context, catalog.uniqueValuesFor('Creator')

    @ram.cache(__call__cachekey)
    def __call__(self, context):
        """ """
        catalog = api.portal.get_tool('portal_catalog')
        res = []
        for creator in catalog.uniqueValuesFor('Creator'):
            fullname = get_user_fullname(creator)
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


@implementer(IVocabularyFactory)
class PloneGroupInterfacesVocabulary(object):
    """List interfaces that will be shown in contacts faceted navigation."""

    def _interfaces(self):
        """ """
        interfaces = [
            IPloneGroupContact,
            INotPloneGroupContact,
        ]
        return interfaces

    def __call__(self, context):
        terms = []
        if HAS_PLONEGROUP:
            terms = [SimpleVocabulary.createTerm(
                interface.__identifier__,
                interface.__identifier__,
                _(interface.__name__))
                for interface in self._interfaces()]

        return SimpleVocabulary(terms)


PloneGroupInterfacesVocabularyFactory = PloneGroupInterfacesVocabulary()


@implementer(IVocabularyFactory)
class ContactsReviewStatesVocabulary(object):
    """ Contacts states vocabulary """

    def __call__(self, context):
        terms = []
        wfTool = api.portal.get_tool('portal_workflow')
        # keep every states of every contact portal_types
        org_wfs = wfTool.getWorkflowsFor('organization') + \
            wfTool.getWorkflowsFor('person') + wfTool.getWorkflowsFor('held_position')
        # avoid duplicates
        state_ids = []
        for org_wf in org_wfs:
            for state in org_wf.states.values():
                state_id = state.id
                if state_id not in state_ids:
                    state_ids.append(state_id)
                    terms.append(SimpleVocabulary.createTerm(
                        state.id,
                        state.id,
                        translate(safe_unicode(state.title),
                                  domain='plone',
                                  context=context.REQUEST)))
        return SimpleVocabulary(terms)


ContactsReviewStatesVocabularyFactory = ContactsReviewStatesVocabulary()
