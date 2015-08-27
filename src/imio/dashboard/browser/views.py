# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView

from imio.dashboard.adapters import CURRENT_CRITERION


class RenderTermPortletView(BrowserView):

    selected_term = ''

    def __call__(self, term, category, widget):
        self.term = term
        self.category = category
        self.widget = widget
        session = self.request.get('SESSION', {})
        if session.has_key(CURRENT_CRITERION):  # noqa
            self.selected_term = session[CURRENT_CRITERION]

        return self.index()
