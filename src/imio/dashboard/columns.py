# encoding: utf-8
from collective.eeafaceted.z3ctable.columns import TitleColumn
from imio.prettylink.interfaces import IPrettyLink


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
