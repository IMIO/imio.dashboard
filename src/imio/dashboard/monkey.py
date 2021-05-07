# encoding: utf-8
from imio.dashboard import logger
from imio.helpers import content as content_helper
from collective.eeafaceted.z3ctable import columns as z3ctable_columns


# Monkey patch get_user_fullname from eeafaceted.z3ctable
# to add compatibility with pas.plugins.imio for the 'Creator' column
z3ctable_columns.get_user_fullname = content_helper.get_user_fullname
logger.info("Monkey patching collective.eeafaceted.z3ctable.get_user_fullname (imio.helpers.get_user_fullname)")
