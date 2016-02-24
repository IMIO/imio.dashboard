# -*- coding: utf-8 -*-
"""Test views."""
import json

from plone import api

from imio.dashboard.testing import IntegrationTestCase


class TestJSONCollectionsCount(IntegrationTestCase):

    def setUp(self):
        super(TestJSONCollectionsCount, self).setUp()
        self.view = self.folder.unrestrictedTraverse('@@json_collections_count')

    def test_folder_empty(self):
        expected = json.dumps([])
        self.assertEqual(self.view(), expected)

    def test_with_collections(self):
        dashboardcoll = api.content.create(
            id='dc1',
            type='DashboardCollection',
            title='Dashboard collection 1',
            container=self.folder
        )
        dashboardcol2 = api.content.create(
            id='dc2',
            type='DashboardCollection',
            title='Dashboard collection 2',
            container=self.folder
        )
        dashboardcoll.query = [
            {
                'i': 'portal_type',
                'o': 'plone.app.querystring.operation.selection.is',
                'v': ['DashboardCollection', ]
            },
        ]
        expected = [
            {'uid': dashboardcoll.UID(), 'count': 2},
            {'uid': dashboardcol2.UID(), 'count': 0},
        ]
        self.assertEqual(self.view(), json.dumps(expected))
