# -*- coding: utf-8 -*-
import pkg_resources

from plone import api
from plone.portlets.interfaces import IPortletRetriever, IPortletManager
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility, getMultiAdapter

from imio.dashboard.adapters import CURRENT_CRITERION
from collective.eeafaceted.collectionwidget.browser.views import RenderTermView as BaseRenderTermView


class RenderTermView(BaseRenderTermView):

    index = ViewPageTemplateFile(
        pkg_resources.resource_filename(
            'collective.eeafaceted.collectionwidget',
            'browser/templates/term.pt'))

    def display_number_of_items(self):
        """Display number of items in the collection."""
        return self.context.getShowNumberOfItems() or False


class RenderTermPortletView(BaseRenderTermView):

    selected_term = ''

    def display_number_of_items(self):
        """Display number of items in the collection."""
        return self.context.getShowNumberOfItems() or False

    def __call__(self, term, category, widget):
        self.term = term
        self.category = category
        self.widget = widget
        pqi = api.portal.get_tool('portal_quickinstaller')
        if pqi.isProductInstalled('collective.querynextprev'):
            session = self.request.get('SESSION', {})
            if session.has_key(CURRENT_CRITERION):  # noqa
                self.selected_term = session[CURRENT_CRITERION]

        return self.index()


class FakeView(BrowserView):
    """
    Portlet manager code goes down well with cyanide.
    """


def get_portlet_manager(column):
    """ Return one of default Plone portlet managers.
    @param column: "plone.leftcolumn" or "plone.rightcolumn"
    @return: plone.portlets.interfaces.IPortletManagerRenderer instance
    """
    manager = getUtility(IPortletManager, name=column)
    return manager


class AjaxRenderDashboardPortlet(BrowserView):

    """Render portlet for ajax calls.

    See http://docs.plone.org/develop/plone/functionality/portlets.html#update-and-render
    """

    def __call__(self):
        context = self.context
        manager = get_portlet_manager('plone.leftcolumn')
        request = self.request
        request.set('no_redirect', '1')
        view = FakeView(context, request)
        assignmentId = "portlet_dashboard"
        retriever = getMultiAdapter((context, manager), IPortletRetriever)

        portlets = retriever.getPortlets()

        assignment = None

        if len(portlets) == 0:
            raise RuntimeError("No portlets available for manager %s in the context %s" % (manager.__name__, context))
        for portlet in portlets:

            # portlet is {'category': 'context', 'assignment': <FacebookLikeBoxAssignment at facebook-like-box>, 'name': u'facebook-like-box', 'key': '/isleofback/sisalto/huvit-ja-harrasteet
            # Identify portlet by interface provided by assignment
            print portlet
            if portlet["name"] == assignmentId:
                assignment = portlet["assignment"]
                break

        if assignment is None:
            # Did not find a portlet
            raise RuntimeError("No portlet found with name: %s" % assignmentId)

        # Note: Below is tested only with column portlets

        # PortletManager provides convenience callable
        # which gives you the renderer. The view is mandatory.
        managerRenderer = manager(context, request, view)

        # PortletManagerRenderer convenience function
        renderer = managerRenderer._dataToPortlet(portlet["assignment"].data)

        if renderer is None:
            raise RuntimeError("Failed to get portlet renderer for %s in the context %s" % (assignment, context))

        renderer.update()

        # Does not check visibility here... force render always
        return renderer.widget_render
