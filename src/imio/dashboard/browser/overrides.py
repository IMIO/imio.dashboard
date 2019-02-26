# -*- coding: utf-8 -*-

from collective.eeafaceted.collectionwidget.browser.views import RenderCategoryView
from eea.facetednavigation.browser.app.query import FacetedQueryHandler
from imio.dashboard.config import COMBINED_INDEX_PREFIX
from imio.dashboard.interfaces import IContactsDashboard
from plone import api
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IDRenderCategoryView(RenderCategoryView):
    '''
      Override the way a category is rendered so we add an icon
      to add content when relevant.
    '''

    manage_add_contact_actions = True

    def contact_infos(self):
        return {'orgs-searches': {'typ': 'organization', 'add': '++add++organization', 'img': 'organization_icon.png'},
                'hps-searches': {'typ': 'contact', 'add': '@@add-contact', 'img': 'create_contact.png'},
                'persons-searches': {'typ': 'person', 'add': '++add++person', 'img': 'person_icon.png'},
                'cls-searches': {'typ': 'contact_list', 'add': 'contact-lists-folder',
                                 'img': 'directory_icon.png', 'class': ''}
                }

    def _get_category_template(self):
        if self.manage_add_contact_actions and IContactsDashboard.providedBy(self.context):
            return ViewPageTemplateFile("templates/category_contact.pt")

    def __call__(self, widget):
        self.member = api.user.get_current()
        return super(IDRenderCategoryView, self).__call__(widget)


class CombinedFacetedQueryHandler(FacetedQueryHandler):

    def criteria(self, sort=False, **kwargs):
        """Call original and triturate query to handle 'combined__' prefixed indexes."""
        criteria = super(CombinedFacetedQueryHandler, self).criteria(sort=sort, **kwargs)
        res = criteria.copy()
        for key, value in criteria.items():
            if key == 'facet.field':
                res[key] = [e for e in value
                            if not e.startswith(COMBINED_INDEX_PREFIX)]
            # bypass if it is not a 'combined' index
            if not key.startswith(COMBINED_INDEX_PREFIX):
                continue

            real_index = key.replace(COMBINED_INDEX_PREFIX, '')
            # if we have both real existing index and the 'combined__' prefixed one, combinate it
            if real_index in criteria:
                # combine values to real index
                real_index_values = criteria[real_index]['query']
                if not hasattr(real_index_values, '__iter__'):
                    real_index_values = [real_index_values]
                combined_index_values = criteria[key]['query']
                if not hasattr(combined_index_values, '__iter__'):
                    combined_index_values = [combined_index_values]
                combined_values = []
                for value in combined_index_values:
                    for real_index_value in real_index_values:
                        combined_values.append(real_index_value + '__' + value)
                # update real_index and pop current key
                res[real_index]['query'] = combined_values
                res.pop(key)
            # if we have only the 'combined__' prefixed one, use it as real index
            elif real_index not in criteria:
                res[real_index] = value
        return res
