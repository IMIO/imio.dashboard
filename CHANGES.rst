Changelog
=========


0.4 (unreleased)
----------------

- Nothing changed yet.


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
