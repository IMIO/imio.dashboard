# -*- coding: utf-8 -*-
import os
from collective.eeafaceted.collectionwidget.widgets.widget import CollectionWidget
from eea.facetednavigation.interfaces import ICriteria
from eea.facetednavigation.interfaces import IFacetedLayout
from eea.facetednavigation.interfaces import IFacetedNavigable
from eea.facetednavigation.interfaces import IHidePloneLeftColumn

from imio.dashboard.testing import IntegrationTestCase
from imio.dashboard.utils import enableFacetedDashboardFor
from imio.dashboard.utils import getCollectionLinkCriterion
from imio.dashboard.utils import getCurrentCollection
from imio.dashboard.utils import NoFacetedViewDefinedException
from imio.dashboard.utils import _updateDefaultCollectionFor


class TestUtils(IntegrationTestCase):
    """Test the utils."""

    def test_getCollectionLinkCriterion(self):
        """This method will return the Collection-link widget defined on a folder if ever."""
        # self.folder is faceted enabled
        self.assertEquals(getCollectionLinkCriterion(self.folder).widget,
                          CollectionWidget.widget_type)
        # remove the criterion then try to get it again
        ICriteria(self.folder).delete(getCollectionLinkCriterion(self.folder).getId())
        self.assertEquals(getCollectionLinkCriterion(self.folder), None)
        # trying to get collection-link widget on a folder that is not
        # faceted enabled will raise a NoFacetedViewDefinedException
        folder2_id = self.portal.invokeFactory('Folder', 'folder2', title='Folder2')
        folder2 = getattr(self.portal, folder2_id)
        self.assertRaises(NoFacetedViewDefinedException, getCollectionLinkCriterion, folder2)

    def test_getCurrentCollection(self):
        """Returns the Collection currently used by the CollectionWidget in a faceted."""
        # add a DashboardCollection to self.folder
        dashcoll_id = self.folder.invokeFactory('DashboardCollection', 'dashcoll', title='Dashboard Collection')
        dashcoll = getattr(self.folder, dashcoll_id)
        dashcoll.reindexObject()

        # current collection is get with collectionLink id in the REQUEST, not set for now
        criterion = getCollectionLinkCriterion(self.folder)
        criterion_name = '{0}[]'.format(criterion.__name__)
        request = self.portal.REQUEST
        self.assertFalse(criterion_name in request)
        self.assertIsNone(getCurrentCollection(self.folder))

        # set a correct collection in the REQUEST
        request.form[criterion_name] = dashcoll.UID()
        self.assertEquals(getCurrentCollection(self.folder), dashcoll)

    def test_enableFacetedDashboardFor(self):
        """This method will enable the faceted navigation for a given folder."""
        # faceted can be enabled using the default widgets
        catalog = self.portal.portal_catalog
        folder2_id = self.portal.invokeFactory('Folder', 'folder2', title='Folder2')
        folder2 = getattr(self.portal, folder2_id)
        folder2.reindexObject()
        folder2UID = folder2.UID()
        # not enabled for now
        self.assertFalse(IFacetedNavigable.providedBy(folder2))
        self.assertTrue(catalog(UID=folder2UID))
        self.assertFalse(catalog(UID=folder2UID, object_provides=IFacetedNavigable.__identifier__))
        enableFacetedDashboardFor(folder2)
        # several things are done :
        # faceted is enabled
        self.assertTrue(IFacetedNavigable.providedBy(folder2))
        # used faceted layout is 'faceted-table-items'
        self.assertEquals(IFacetedLayout(folder2).layout, 'faceted-table-items')
        # left portlets are shown
        self.assertFalse(IHidePloneLeftColumn.providedBy(folder2))
        # folder2 was reindexed, especially provided interfaces
        self.assertTrue(catalog(UID=folder2UID, object_provides=IFacetedNavigable.__identifier__))
        # redirect is swallowed, indeed enabling faceted on a folder redirects to it
        self.assertEquals(self.portal.REQUEST.RESPONSE.status, 200)

        # a xmlpath parameter can be passed to use a specific widgets xml file
        # calling this on an already enabled faceted will do nothing
        xmlpath = os.path.dirname(__file__) + '/faceted_conf/testing_widgets.xml'
        enableFacetedDashboardFor(folder2, xmlpath=xmlpath)
        # only one 'c44' widget in testing_widget.xml, not added here
        self.assertFalse(ICriteria(folder2).get('c44'))
        # create a new folder and apply faceted with xmlpath to it
        folder3_id = self.portal.invokeFactory('Folder', 'folder3', title='Folder3')
        folder3 = getattr(self.portal, folder3_id)
        folder3.reindexObject()
        # an Exception is raised if xmlpath does not exist
        wrong_xmlpath = os.path.dirname(__file__) + '/faceted_conf/wrong_testing_widgets.xml'
        self.assertRaises(Exception, enableFacetedDashboardFor, folder3, wrong_xmlpath)
        # apply correct xmlpath
        enableFacetedDashboardFor(folder3, xmlpath=xmlpath)
        # same things are done except that the widgets are taken from the given xmlpath
        self.assertEquals(len(ICriteria(folder3).criteria), 1)
        self.assertTrue(ICriteria(folder3).get('c44'))

    def test_updateDefaultCollectionFor(self):
        """This method will define the default collection used by the collection-link
           widget defined in a faceted enabled folder."""
        # get the collection-link and check that it has no default
        criterion = getCollectionLinkCriterion(self.folder)
        self.assertFalse(criterion.default)
        # right, do things correctly, add a DashboardCollection and use it as default
        dashcoll_id = self.folder.invokeFactory('DashboardCollection', 'dashcoll', title='Dashboard Collection')
        dashcoll = getattr(self.folder, dashcoll_id)
        dashcoll.reindexObject()
        _updateDefaultCollectionFor(self.folder, dashcoll.UID())
        self.assertEquals(criterion.default, dashcoll.UID())

        # calling it on a non faceted enabled folder will raise a NoFacetedViewDefinedException
        folder2_id = self.portal.invokeFactory('Folder', 'folder2', title='Folder2')
        folder2 = getattr(self.portal, folder2_id)
        folder2.reindexObject()
        self.assertRaises(NoFacetedViewDefinedException, _updateDefaultCollectionFor, folder2, 'anUID')
