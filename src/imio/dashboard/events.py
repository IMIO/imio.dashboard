# encoding: utf-8
import logging
log = logging.getLogger('imio.dashboard')


def onMonkeyPatched(event):
    '''Add a message to the log when a method has been monkey patched.'''
    log.info("Monkey patching %s with %s : %s" % (event.original, event.replacement, event.description))
