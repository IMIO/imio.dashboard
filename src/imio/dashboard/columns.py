# encoding: utf-8

from collective.eeafaceted.z3ctable.columns import BrowserViewCallColumn


class ActionsColumn(BrowserViewCallColumn):
    """
    A column displaying available actions of the listed item.
    """

    header_js = '<script type="text/javascript">jQuery(document).ready(initializeOverlays);' \
                'jQuery(document).ready(preventDefaultClickTransition);</script>'
    view_name = 'actions_panel'
    params = {'showHistory': True, 'showActions': True}
