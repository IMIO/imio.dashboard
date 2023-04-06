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


Combined indexes :
------------------
Sometime you build an index made of the concatenation of some subindexes to workaround ZCatalog weakness.
In this case, you could need several faceted filters to query theses indexes, it is possible with combined indexes.

Let's say you have an index for portal_type Folder that stores the portal_type and review_state of contained objects.
The index ``contained_with_review_state`` content could looks like :

.. code:: python

  ['Document__private', 'Document__published', 'Image__private']

Now if you want to display in a dashboard folders containing ``Documents`` that are in state ``private``,
you will likely use 2 filters :

- the first listing portal_types (``Document``, ``Image``, ``Folder``, ...);
- the second listing review_states (``private``, ``published``, ...).

In the filter list of indexes available, you will have every available portal_catalog indexes and a duplicated
list of these indexes prefixed with ``(Combined)``.  If you select the index ``contained_with_review_state`` for
the filter ``portal_types`` and the ``(Combined) contained_with_review_state`` for the filter ``review_states``, this will
automatically be combined so selecting ``Document`` in first filter and ``private`` in second filter will actually query
for ``Document__private``.
