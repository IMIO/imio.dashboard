# encoding: utf-8

from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.facetednavigation.criteria.interfaces import ICriteria

from imio.dashboard import ImioDashboardMessageFactory as _
from eea.facetednavigation.subtypes.interfaces import IFacetedNavigable


class IFacetedCollectionPortlet(IPortletDataProvider):
    """ A portlet that shows controls for faceted with collections """


class Assignment(base.Assignment):
    implements(IFacetedCollectionPortlet)

    @property
    def title(self):
        return u"Collections widget"


class Renderer(base.Renderer):

    widget_types = ('collection-radio', 'collection-link')

    def render(self):
        return ViewPageTemplateFile('templates/portlet_facetedcollection.pt')(self)

    @property
    def available(self):
        return IFacetedNavigable.providedBy(self.context)

    @property
    def widget_render(self):
        criteria = ICriteria(self.context)
        widgets = []
        for criterion in criteria.values():
            if criterion.widget not in self.widget_types:
                continue
            widget_cls = criteria.widget(wid=criterion.widget)
            widgets.append(widget_cls(self.context, self.request, criterion))
        return ''.join([w() for w in widgets])


class AddForm(base.AddForm):
    form_fields = form.Fields(IFacetedCollectionPortlet)
    label = _(u"Add Collection Criteria Portlet")
    description = _(u"This portlet shows controls for faceted with collections.")

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    form_fields = form.Fields(IFacetedCollectionPortlet)
    label = _(u"Edit Collection Criteria Portlet")
    description = _(u"This portlet shows controls for faceted with collections.")
