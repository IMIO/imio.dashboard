# -*- coding: utf-8 -*-

from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IImioDashboardLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class ICustomViewFieldsVocabulary(Interface):
    """
      Adapter interface that manage override of the
      plone.app.collection Collection.customViewFields vocabulary.
    """

    def listMetaDataFields(self, exclude=True):
        """
          Works the same way as the Collection.customViewFields vocabulary but get additionalViewFields.
        """

    def additionalViewFields(self):
        """
          Additional fields taken into account by the listMetaDataFields vocabulary.
        """
