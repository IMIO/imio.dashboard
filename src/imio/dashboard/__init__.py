# -*- coding: utf-8 -*-
"""Init and utils."""

from zope.i18nmessageid import MessageFactory
import logging


ImioDashboardMessageFactory = MessageFactory('imio.dashboard')
logger = logging.getLogger('imio.dashboard')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
