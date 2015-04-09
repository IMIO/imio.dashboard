# encoding: utf-8

from Acquisition import aq_inner, aq_parent

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
        return bool(self._criteriaHolder)

    @property
    def widget_render(self):
        # get the IFacetedNavigable element the criteria are define on
        criteriaHolder = self._criteriaHolder
        criteria = ICriteria(criteriaHolder)
        widgets = []
        for criterion in criteria.values():
            if criterion.widget not in self.widget_types:
                continue
            widget_cls = criteria.widget(wid=criterion.widget)
            widget = widget_cls(criteriaHolder, self.request, criterion)
            widget.display_fieldset = False
            # if current context does not provide IFacetedNavigable it means
            # that the portlet is displayed on children, we use another template
            # for rendering the widget
            rendered_widget = widget()
            if not IFacetedNavigable.providedBy(self.context):
                widget.criteria_holder_url = criteriaHolder.absolute_url()
                rendered_widget = ViewPageTemplateFile('templates/widget.pt')(widget)
            widgets.append(rendered_widget)
        return ''.join([w for w in widgets])

    @property
    def _criteriaHolder(self):
        '''Get the element the criteria are defined on.  This will look up parents until
           a folder providing IFacetedNavigable is found.'''
        parent = self.context
        # look up parents until we found the criteria holder or we reach the 'Plone Site'
        while parent:
            if IFacetedNavigable.providedBy(parent):
                return parent
            parent = aq_parent(aq_inner(parent))
            if parent.portal_type == 'PloneSite':
                return None


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
