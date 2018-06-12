# -*- coding: utf-8 -*-
from eea.facetednavigation.browser.app.query import FacetedQueryHandler
from imio.dashboard.config import COMBINED_INDEX_PREFIX


class CombinedFacetedQueryHandler(FacetedQueryHandler):

    def criteria(self, sort=False, **kwargs):
        """Call original and triturate query to handle 'combined__' prefixed indexes."""
        criteria = super(CombinedFacetedQueryHandler, self).criteria(sort=sort, **kwargs)
        res = criteria.copy()
        for key, value in criteria.items():
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
