# encoding: utf-8
from collective.eeafaceted.z3ctable.columns import BrowserViewCallColumn
from collective.eeafaceted.z3ctable.columns import TitleColumn
from imio.prettylink.interfaces import IPrettyLink


class ActionsColumn(BrowserViewCallColumn):
    """A column that display the result of a given browser view name call."""

    def renderHeadCell(self):
        """Override rendering of head of the cell to include jQuery
           call to initialize overlays used by differents actions (transitions popup, history, ...)."""
        header = '<script type="text/javascript">jQuery(document).ready(initializeOverlays);</script>{0}'
        return header.format(super(ActionsColumn, self).renderHeadCell())


class PrettyLinkColumn(TitleColumn):
    """A column that display the IPrettyLink.getLink column."""

    @property
    def cssClasses(self):
        """Generate a CSS class for each <th> so we can skin it if necessary."""
        cssClasses = super(PrettyLinkColumn, self).cssClasses.copy() or {}
        cssClasses.update({'td': 'pretty_link', })
        return cssClasses

    def renderCell(self, item):
        """ """
        obj = self._getObject(item)
        return IPrettyLink(obj).getLink()
