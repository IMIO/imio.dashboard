# -*- coding: utf-8 -*-

import logging
from collective.documentgenerator.content.pod_template import ConfigurablePODTemplate
from collective.documentgenerator.content.pod_template import IConfigurablePODTemplate
from imio.dashboard import ImioDashboardMessageFactory as _
from plone.autoform import directives as form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implements
logger = logging.getLogger('imio.dashboard: DashboardPODTemplate')

################################################################################
#                                                                              #
#  DEPRECATED, THIS CONTENT WAS MOVED TO COLLECTIVE.EEAFACETED.DASHBOARD !!!   #
#                                                                              #
#  STILL EXISTS FOR MIGRATION PURPOSE !!!                                      #
#                                                                              #
################################################################################


class IDashboardPODTemplate(IConfigurablePODTemplate):
    """
    DashboardPODTemplate dexterity schema.
    """

    use_objects = schema.Bool(
        title=_(u'Use objects as generation context'),
        description=_(u'If selelected, receive awoken objects wrapped into their '
                      u' helper view rather than brains as generation context'),
        default=False,
        required=False,
    )

    form.widget('dashboard_collections', CheckBoxFieldWidget, multiple='multiple', size=15)
    dashboard_collections = schema.List(
        title=_(u'Allowed dashboard collections'),
        description=_(u'Select for which dashboard collections the template will be available. '
                      u'If nothing is selected, the template will be available on every dashboards.'),
        value_type=schema.Choice(source='imio.dashboard.collectionsvocabulary'),
        required=True,
    )
    form.omitted('pod_portal_types')


class DashboardPODTemplate(ConfigurablePODTemplate):
    """
    DashboardPODTemplate dexterity class.
    """

    implements(IDashboardPODTemplate)
