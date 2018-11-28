# encoding: utf-8
from collective.eeafaceted.z3ctable.columns import PrettyLinkColumn


class ContactPrettyLinkColumn(PrettyLinkColumn):

    attrName = 'get_full_title'
    params = {
        'showContentIcon': True,
        'target': '_blank',
        'additionalCSSClasses': ['link-tooltip'],
        'display_tag_title': False}

    def contentValue(self, item):
        """ """
        return getattr(item, self.attrName)()

    def renderCell(self, item):
        """ """
        obj = self._getObject(item)
        return super(ContactPrettyLinkColumn, self).getPrettyLink(obj)
