# -*- coding: utf-8 -*-

import logging
from imio.migrator.migrator import Migrator
from plone.app.contenttypes.migration.dxmigration import ContentMigrator
from plone.app.contenttypes.migration.migration import CollectionMigrator
from plone.app.contenttypes.migration.migration import migrate as pac_migrate
from plone.dexterity.utils import iterSchemataForType
from zope.interface.interfaces import IMethod
from zope.schema import getFieldsInOrder

logger = logging.getLogger('imio.dashboard')


class DashboardPODTemplateMigrator(ContentMigrator):
    """ """
    src_portal_type = 'DashboardPODTemplate'
    src_meta_type = 'Dexterity Item'
    dst_portal_type = 'DashboardPODTemplate'
    dst_meta_type = None  # not used

    def migrate_schema_fields(self):
        for schemata in iterSchemataForType('DashboardPODTemplate'):
            for fieldName, field in getFieldsInOrder(schemata):
                # bypass interface methods
                if not IMethod.providedBy(field):
                    # special handling for file field
                    setattr(self.new, fieldName, getattr(self.old, fieldName))


class DashboardCollectionMigrator(CollectionMigrator):
    """ """
    src_portal_type = 'DashboardCollection'
    src_meta_type = 'DashboardCollection'
    dst_portal_type = 'DashboardCollection'
    dst_meta_type = None  # not used

    def migrate_schema_fields(self):
        super(DashboardCollectionMigrator, self).migrate_schema_fields()
        # due to a bug, Bool that are False are not migrated...
        self.new.sort_reversed = self.old.sort_reversed
        # migrate custom field manually
        self.new.showNumberOfItems = self.old.showNumberOfItems
        # fields from ITALCondition extender
        self.new.tal_condition = self.old.tal_condition
        self.new.roles_bypassing_talcondition = self.old.roles_bypassing_talcondition


class Migrate_To_6(Migrator):

    def __init__(self, context):
        Migrator.__init__(self, context)

    def run(self):
        logger.info('Migrating to imio.dashboard 6...')
        # install collective.eeafaceted.dashboard before migrating so portal_types are correct
        self.reinstall(['profile-collective.eeafaceted.dashboard:default'])
        pac_migrate(self.portal, DashboardPODTemplateMigrator)
        pac_migrate(self.portal, DashboardCollectionMigrator)
        # pac migration do not reindex migrated objects
        brains = self.portal.portal_catalog(portal_type=['DashboardCollection', 'DashboardPODTemplate'])
        for brain in brains:
            collection = brain.getObject()
            collection.reindexObject()
        self.cleanRegistries()
        self.finish()


def migrate(context):
    '''
    '''
    Migrate_To_6(context).run()
