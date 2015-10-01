.. image:: https://travis-ci.org/IMIO/imio.dashboard.svg?branch=master
    :target: https://travis-ci.org/IMIO/imio.dashboard
.. image:: https://coveralls.io/repos/IMIO/imio.dashboard/badge.png?branch=master
   :target: https://coveralls.io/r/IMIO/imio.dashboard?branch=master


imio.dashboard
==============

This package does the glue between :

- collective.eeafaceted.collectionwidget
- collective.eeafaceted.z3ctable
- collective.compoundcriterion
- collective.documentgenerator

This build a useable dashboard tool by adapting following things :

- displaying the collectionwidget in a portlet;
- defining an adapter to easily extend the plone.app.collection customViewFields to add our own columns;
- adding a DashboardCollection based on plone.app.collection Collection;
- being able to generate a POD template from what is displayed in a dashboard;
- styling of displayed dashboard.

Distant faceted config :
------------------------
It is possible to define a central faceted config that will be used by different elements that will use it
because getting criteria managed by an only method defined in an adapter, to do so :

In adapters.py :
*******************
.. code:: python

    from eea.facetednavigation.criteria.handler import Criteria as eeaCriteria

    class Criteria(eeaCriteria):
        """ Handle criteria
        """

        def __init__(self, context):
            """ Handle criteria
            """
            super(Criteria, self).__init__(context)
            # let's say we have a centralized faceted config defined at the root and called 'distantfacetedconfig'
            if hasattr(self.context, 'distantfacetedconfig'):
                self.context = self.context.distantfacetedconfig
                self.criteria = self._criteria()

In a overrides.zcml :
*********************
.. code:: xml

  <adapter
    for="eea.facetednavigation.interfaces.IFacetedNavigable"
    provides="eea.facetednavigation.interfaces.ICriteria"
    factory=".adapters.Criteria" />
