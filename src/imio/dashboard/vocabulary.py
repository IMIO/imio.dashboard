# encoding: utf-8

from zope.schema.vocabulary import SimpleVocabulary

from collective.behavior.talcondition.interfaces import ITALConditionable
from collective.behavior.talcondition.utils import evaluateExpressionFor
from collective.eeafaceted.collectionwidget.vocabulary import CollectionVocabulary

from Products.CMFCore.utils import getToolByName


class ConditionAwareCollectionVocabulary(CollectionVocabulary):

    def __call__(self, context, query=None):
        """Same behaviour as the original CollectionVocabulary
           but we will filter Collections regarding the defined tal_condition."""
        terms = super(ConditionAwareCollectionVocabulary, self).__call__(context, query=query)

        catalog = getToolByName(context, 'portal_catalog')
        filtered_terms = []
        for term in terms:
            collection = catalog(UID=term.token)[0].getObject()
            # if collection is ITALConditionable, evaluate the TAL condition
            # except if current user is Manager
            if ITALConditionable.providedBy(collection):
                if not evaluateExpressionFor(collection, bypass_for_manager=True):
                    continue
            filtered_terms.append(term)
        return SimpleVocabulary(filtered_terms)

ConditionAwareCollectionVocabularyFactory = ConditionAwareCollectionVocabulary()
