Changelog
=========


0.29 (2023-04-06)
-----------------

- Swallow all exceptions when trying to renderding the portlet title.
  [sdelcourt]
- Adapts generation link override to last versions of documentgenerator.
  [sdelcourt]
- Use icons.
  [sdelcourt]
- Docgen icons are now svg.
  [sdelcourt]

0.28 (2017-10-09)
-----------------

- Removed bad class attribute meta_type to avoid paste error
  [sgeulette]

0.27 (2017-08-07)
-----------------

- Add a listing with brains, objects and helper view only available when selection 'use_objects'
  on the dashboard template.
  [sdelcourt]

0.26 (2017-08-02)
-----------------

- Add 'use_objects' attribute on dashboard template if you want to have iterate over the objects
  and their helper view rather than the brains.
  [sdelcourt]

0.25 (2017-03-22)
-----------------

- Use CheckBoxFieldWidget for IDashboardPODTemplate.dashboard_collections to
  ease selection when displaying several elements.
  [gbastien]

0.24 (2017-02-09)
-----------------

- Added javascript variables for i18n.
  [sgeulette]
- Enable merging and caching for imio.dashboard.js in portal_javascripts.
  [gbastien]

0.23 (2017-01-31)
-----------------

- Check if there are some checkboxes on a faceted to get uids.
  [bsuttor]
- Added plone.app.collection as a dependency.
  [gbastien]

0.22 (2016-11-22)
-----------------

- Check if context is provided by IDashboardCollection to count number of dashborad collections.
  [bsuttor]

- Check if context is provided by IDashboardCollection to display_number_of_items.
  [bsuttor]

- Updated _get_generation_context to add needed parameter from documentgenerator.
  Test context variables integration
  [sgeulette]

0.21 (2016-10-05)
-----------------

- Added own doc generation dashboard viewlet.
  Modified generation view to handle both outside or inside dashboard generations.
  [sgeulette]
- Display category in pod template collections vocabulary
  [sgeulette]
- Test exception when getting criterion value.
  [sgeulette]
- Check if we are in dashboard documentgenerator viewlet. For some content with iframe dashboard,
  there can be also a normal documentgenerator viewlet.
  [sgeulette]

0.20 (2016-08-03)
-----------------

- Move columns ordering to collective.eeafaceted.z3ctable
  [sdelcourt]

0.19 (2016-05-13)
-----------------

- Removed invasive styling, not the place here.
  [gbastien]

0.18 (2016-04-15)
-----------------

- Added english translations.
  [sgeulette]
- Make configuration types not displayed in the search, added 'Collection', 'DashboardCollection',
  'Topic', 'ConfigurablePODTemplate', 'DashboardPODTemplate', 'PODTemplate', 'StyleTemplate'
  and 'SubTemplate to site_properties.types_not_searched.
  [gbastien]

0.17 (2016-03-22)
-----------------

- Added meta_type for 'DashboardPODTemplate'.
  [gbastien]
- Fixed JS in generatePodDocument to not generate the Pod template after alert 'no items selected'.
  [gbastien]
- Changed JS generatePodDocument check to know if we are on a faceted page : do not query
  input[name="select_item"] checkboxes as there could be none displayed if current faceted displays
  no result, instead check for presence of div#faceted-results.
  [gbastien]

0.16 (2016-03-03)
-----------------

- Added possibility to display number of collection items in the term view.
  [cedricmessiant]
- Removed unused method CustomViewFieldsVocabularyAdapter.additionalViewFields.
  [gbastien]
- Added params in PrettyLinkColumn. Use it in RelationPrettyLinkColumn and external columns.
  [sgeulette]

0.15 (2016-02-15)
-----------------

- Added RelationPrettyLinkColumn to display with PrettyLink a z3c.relationfield.relation.RelationValue attribute.
  [sgeulette]
- Limit padding left and right of the faceted checkbox widget to 0.2em instead of 1em.
  [gbastien]
- Added 'combined indexes' functionnality making it possible to combinate faceted filters together to
  query a single catalog index.
  [gbastien]
- In utils._updateDefaultCollectionFor as we change the faceted criteria annotations, make sure
  it is persisted by setting _p_changed = True
  [gbastien]

0.14 (2016-01-21)
-----------------

- The POD template description is now displayed when hovering the POD template title.
  [gbastien]

0.13 (2016-01-15)
-----------------

- Consider portlet is outside faceted when adding a new element.
  [sgeulette]
- Use ITopAboveNavManager to display the dashboard POD templates viewlet,
  this is due to a change in collective.eeafaceted.z3ctable where viewlet managers
  were renamed (was ITopManager before).
  [gbastien]

0.12 (2016-01-04)
-----------------

- Adapted CSS regarding sort triangle entities now that we use larger ones.
  [gbastien]

0.11 (2015-12-17)
-----------------

- Format sort triangle entities.
  [sgeulette]
- Define an icon_expr for portal_type DashboardPODTemplate so it is correctly
  displayed in the DX types control panel especially.
  [gbastien]

0.10 (2015-11-27)
-----------------

- Added possibility to pass 'extra_expr_ctx' to evaluateExpressionFor while
  evaluating the TAL condition defined on the DashboardCollection.
  [gbastien]

0.9 (2015-11-24)
----------------

- Added method utils.getDashboardQueryResult that compute 'uids' and 'brains'
  returned by the current faceted query.
  [sdelcourt, gbastien]

- Test if collective.querynextprev is installed before accessing session
  [sgeulette]

0.8 (2015-11-03)
----------------
- Release that corrects the wrong 0.7 release.
  [gbastien]

0.7 (2015-11-03)
----------------
- Give permission 'eea.facetednavigation: Configure faceted'
  only for 'Manager' by default.
  [gbastien]
- Added a submethod utils._get_criterion that gets any widget type
  of a given faceted_context, it is now used by utils.getCollectionLinkCriterion
  and may be used alone if necessary.
  [gbastien]

0.6 (2015-10-08)
----------------
- Omit field 'pod_portal_types' for DashboardPODTemplate, it is useless as it
  is always available for Folders.
  [gbastien]
- Do not fail when extracting facetedQuery values if we receive an 'int'.
  [gbastien]
- Added content_type icon for DashboardPODTemplate.
  [gbastien]

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
- Fix DashboardCollection object name in type definition
  [cedricmessiant]

0.1 (2015-07-14)
----------------
- Added portlet that shows Collection widget defined on a faceted nav enabled folder.
  [gbastien]
- Initial release.
  [IMIO]

