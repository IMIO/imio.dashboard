# encoding: utf-8

from collective.eeafaceted.z3ctable.columns import PrettyLinkColumn

import pkg_resources

HAS_CONTACT_CORE = True
try:
    pkg_resources.get_distribution('collective.contact.core')
    from collective.contact.core.content.organization import IOrganization
except pkg_resources.DistributionNotFound:
    HAS_CONTACT_CORE = False


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

    def getCSSClasses(self, item):
        """Returns a CSS class specific to current content."""
        cssClasses = super(ContactPrettyLinkColumn, self).getCSSClasses(item)

        current_org_css_class = None
        obj = self._getObject(item)
        if HAS_CONTACT_CORE and IOrganization.providedBy(obj):
            current_org_css_class = '___'.join([org.id for org in obj.get_organizations_chain()])

        if current_org_css_class:
            cssClasses['td'] = '{0} {1}'.format(cssClasses['td'], current_org_css_class)

        return cssClasses
