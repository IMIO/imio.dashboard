# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IImioDashboardLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IDashboardCollection(Interface):
    """DashboardCollection marker interface"""


class ICustomViewFieldsVocabulary(Interface):
    """
      Adapter interface that manage override of the
      plone.app.collection Collection.customViewFields vocabulary.
    """

    def listMetaDataFields(self, exclude=True):
        """
          Get every IFacetedColumn z3c.table columns.
        """


class NotDashboardContextException(Exception):
    """ To be raised when a context has no faceted view defined on it. """


class NoFacetedViewDefinedException(NotDashboardContextException):
    """ To be raised when a context has no faceted view defined on it. """


class NoCollectionWidgetDefinedException(NotDashboardContextException):
    """ To be raised when a context has no collection widget defined on it. """
