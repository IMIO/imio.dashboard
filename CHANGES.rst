Changelog
=========


0.5 (2015-10-01)
----------------
- Rely on collective.documentgenerator and override the 'document-generation' view
  and the 'generationlink' viewlet so it is possible to generate a document from
  elements displayed in a dashboard.
  [gbastien]
- Added helper method utils.getCurrentCollection that will return the current
  collection used by a CollectionWidget in a faceted.
  [gbastien]
- Rely on Products.ZCatalog >= 3 to be able to use 'not:' statement in queries.
  [gbastien]
- Add DashboardPODtemplate type. This type of pod template is configurable to
  choose on which dashboard it is available/generable.
  [sdelcourt]


0.4 (2015-09-04)
----------------
- Moved 'sorting' and 'collection-link' criteria top 'top/default'
  position to be sure that it is evaluated first by faceted query.
  [gbastien]
- Add adapter for collective.querynextprev integration.
  [cedricmessiant]
- Added a creatorsvocabulary listing creators of the site,
  available especially for faceted criteria.
  [gbastien]
- Added helpers methods utils.getCollectionLinkCriterion and
  utils._updateDefaultCollectionFor.
  [sdelcourt]


0.3 (2015-08-21)
----------------
- Added utils method to enable faceted dashboard on an object and import xml configuration file.
  [sgeulette]


0.2 (2015-08-04)
----------------
- Factorized code that check if we are outside the faceted in the portlet
  so it is easy to override without overriding the entire widget_render method.
  [gbastien]
- Create the "imio.dashboard: Add DashboardCollection" permission in ZCML
  [cedricmessiant]
-  Fix DashboardCollection object name in type definition
  [cedricmessiant]


0.1 (2015-07-14)
----------------
- Added portlet that shows Collection widget defined on a faceted nav enabled folder.
  [gbastien]
- Initial release.
  [IMIO]
