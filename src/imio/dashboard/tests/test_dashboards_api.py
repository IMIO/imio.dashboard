# -*- coding: utf-8 -*-
from imio.dashboard.testing import FunctionalTestCase
from plone import api
from plone.restapi.testing import RelativeSession
from Products.CMFCore.utils import getToolByName


class TestDashboardsAPI(FunctionalTestCase):
    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        self.request = self.portal.REQUEST
        self.catalog = getToolByName(self.portal, "portal_catalog")

        api.user.create(username="cedric", password="no", email="cedric@imio.be")
        import transaction
        transaction.commit()

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = ("cedric", "no")
        self.anon_api_session = RelativeSession(self.portal_url)
        self.anon_api_session.headers.update({"Accept": "application/json"})

    def tearDown(self):
        self.api_session.close()

    def test_anonymous_dashboards(self):
        response = self.anon_api_session.get("/@dashboards")
        self.assertEqual(401, response.status_code)

    def test_simple_dashboards(self):
        response = self.api_session.get("/@dashboards")
        self.assertEqual(200, response.status_code)
        response_body = response.json()
        self.assertEqual([u"folder"], response_body.keys())
