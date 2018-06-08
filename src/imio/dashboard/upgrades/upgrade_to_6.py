# -*- coding: utf-8 -*-

import logging
from collective.eeafaceted.dashboard.content.pod_template import DashboardPODTemplate
from imio.dashboard.content.pod_template import DashboardPODTemplate as old_DashboardPODTemplate
from imio.migrator.migrator import Migrator
from plone.app.contenttypes.migration.migration import CollectionMigrator
from plone.app.contenttypes.migration.migration import migrate as pac_migrate
logger = logging.getLogger('imio.dashboard')


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

    def _migrateDashboardPodTemplateClass(self):
        """The DashboardPodTemplate class changed as content definition was
           moved from imio.dashboard to collective.eeafaceted.dashboard."""
        logger.info('Migrating __class__ attribute for DashboardPODTemplate objects...')
        brains = self.portal.portal_catalog(portal_type='DashboardPODTemplate')
        for brain in brains:
            template = brain.getObject()
            if template.__class__ == old_DashboardPODTemplate:
                template.__class__ = DashboardPODTemplate
                template._p_changed = True
        logger.info('Done.')

    def run(self):
        logger.info('Migrating to imio.dashboard 6...')
        # install collective.eeafaceted.dashboard before migrating so portal_types are correct
        self.reinstall(['profile-collective.eeafaceted.dashboard:default'])
        pac_migrate(self.portal, DashboardCollectionMigrator)
        # pac migration do not reindex migrated objects
        brains = self.portal.portal_catalog(portal_type='DashboardCollection')
        for brain in brains:
            collection = brain.getObject()
            collection.reindexObject()
        self._migrateDashboardPodTemplateClass()
        self.cleanRegistries()
        self.finish()


def migrate(context):
    '''
    '''
    Migrate_To_6(context).run()
