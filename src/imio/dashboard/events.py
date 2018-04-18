# -*- coding: utf-8 -*-
#
# File: events.py
#
# Copyright (c) 2018 by Imio.be
#
# GNU General Public License (GPL)
#

from imio.helpers.cache import invalidate_cachekey_volatile_for


def onDashboardCollectionModified(obj, event):
    '''Called whenever a DashboardCollection is modified.'''
    invalidate_cachekey_volatile_for('imio.dashboard.conditionawarecollectionvocabulary')
