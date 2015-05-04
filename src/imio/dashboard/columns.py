# encoding: utf-8
from collective.eeafaceted.z3ctable.columns import BrowserViewCallColumn


class ActionsColumn(BrowserViewCallColumn):
    """A column that display the result of a given browser view name call."""

    def renderHeadCell(self):
        """Override rendering of head of the cell to include jQuery
           call to initialize overlays used by differents actions (transitions popup, history, ...)."""
        header = '<script type="text/javascript">jQuery(document).ready(initializeOverlays);</script>{0}'
        return header.format(super(ActionsColumn, self).renderHeadCell())
