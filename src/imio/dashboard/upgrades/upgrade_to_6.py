# -*- coding: utf-8 -*-

import logging
from collective.eeafaceted.dashboard.browser.facetedcollectionportlet import Assignment as new_dashboard_portlet
from imio.migrator.migrator import Migrator
from imio.dashboard.browser.facetedcollectionportlet import Assignment as old_dashboard_portlet
from plone.app.contenttypes.migration.dxmigration import ContentMigrator
from plone.app.contenttypes.migration.migration import CollectionMigrator
from plone.app.contenttypes.migration.migration import migrate as pac_migrate
from plone.app.portlets.interfaces import IPortletManager
from plone.app.portlets.interfaces import IPortletAssignmentMapping
from plone.dexterity.utils import iterSchemataForType
from Products.GenericSetup.tool import DEPENDENCY_STRATEGY_IGNORE
from zope.component import getUtility
from zope.component import getMultiAdapter
from zope.interface.interfaces import IMethod
from zope.schema import getFieldsInOrder

logger = logging.getLogger('imio.dashboard')


class DashboardPODTemplateMigrator(ContentMigrator):
    """For DashboardPODTemplates created after imio.dashboard 0.28 where
       meta_type was removed and so 'Dexterity Item' by default."""
    src_portal_type = 'DashboardPODTemplate'
    src_meta_type = 'Dexterity Item'
    dst_portal_type = 'DashboardPODTemplate'
    dst_meta_type = None  # not used

    def migrate_atctmetadata(self):
        """Override to not migrate exclude_from_nav because it does not exist by default
           and it takes parent's value that is an instancemethod and fails at transaction commit..."""
        pass

    def migrate_schema_fields(self):
        for schemata in iterSchemataForType('DashboardPODTemplate'):
            for fieldName, field in getFieldsInOrder(schemata):
                # bypass interface methods
                if not IMethod.providedBy(field):
                    # special handling for file field
                    setattr(self.new, fieldName, getattr(self.old, fieldName, None))


class DashboardPODTemplateMigratorWithDashboardPODTemplateMetaType(DashboardPODTemplateMigrator):
    """For DashboardPODTemplates created before imio.dashboard 0.28 where
       meta_type was defined to 'DashboardPODTemplate'."""
    src_portal_type = 'DashboardPODTemplate'
    src_meta_type = 'DashboardPODTemplate'
    dst_portal_type = 'DashboardPODTemplate'
    dst_meta_type = None  # not used


class DashboardCollectionMigrator(CollectionMigrator):
    """ """
    src_portal_type = 'DashboardCollection'
    src_meta_type = 'DashboardCollection'
    dst_portal_type = 'DashboardCollection'
    dst_meta_type = None  # not used

    def migrate_atctmetadata(self):
        """Override to not migrate exclude_from_nav because it does not exist by default
           and it takes parent's value that is an instancemethod and fails at transaction commit..."""
        pass

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

    def _migrateDashboardPortlet(self):
        """Dashboard portlet was moved to collective.eeafaceted.dashboard, we
           need to find it and migrate the assignment."""
        logger.info('Migrating dashboard portlets...')
        # this will only take into account Plone Site and Folders as portlet holders
        manager = getUtility(IPortletManager, name=u"plone.leftcolumn")
        brains = self.portal.portal_catalog(portal_type=['Folder', 'projectspace'])
        objs = [brain.getObject() for brain in brains]
        objs.insert(0, self.portal)
        for obj in objs:
            assignment_mapping = getMultiAdapter((obj, manager), IPortletAssignmentMapping)
            for k, v in assignment_mapping.items():
                if isinstance(v, old_dashboard_portlet):
                    idx = assignment_mapping._order.index(k)  # get portlet position
                    del assignment_mapping[k]
                    assignment_mapping[k] = new_dashboard_portlet()
                    del assignment_mapping._order[-1]  # del new portlet position
                    assignment_mapping._order.insert(idx, k)  # put new portlet at same position
                    logger.info('Portlet was updated for {0}'.format('/'.join(obj.getPhysicalPath())))
        logger.info('Done.')

    def run(self):
        logger.info('Migrating to imio.dashboard 6...')
        # run eea.facetednavigation upgrade step first so new JS are registered
        # and we insert our after eea.facetednavigation ones
        self.upgradeProfile('eea.facetednavigation:default')
        # install collective.eeafaceted.dashboard before migrating so portal_types are correct
        self.ps.runAllImportStepsFromProfile(
            'profile-collective.eeafaceted.dashboard:universal',
            dependency_strategy=DEPENDENCY_STRATEGY_IGNORE)
        self.reinstall(['profile-collective.eeafaceted.dashboard:default'])
        self.upgradeProfile('collective.eeafaceted.collectionwidget:default')
        pac_migrate(self.portal, DashboardPODTemplateMigrator)
        pac_migrate(self.portal, DashboardPODTemplateMigratorWithDashboardPODTemplateMetaType)
        pac_migrate(self.portal, DashboardCollectionMigrator)
        # pac migration do not reindex migrated objects
        brains = self.portal.portal_catalog(portal_type=['DashboardCollection', 'DashboardPODTemplate'])
        for brain in brains:
            collection = brain.getObject()
            collection.reindexObject()
        self._migrateDashboardPortlet()
        self.cleanRegistries()
        self.finish()


def migrate(context):
    '''Handler to launch migration.'''
    Migrate_To_6(context).run()
