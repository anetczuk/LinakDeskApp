#
#
#

import logging

try:
    import matplotlib

    # Make sure that we are using QT5
    matplotlib.use('Qt5Agg')

    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
except ImportError:
    ### No module named <name>
    logging.exception("Exception while importing")
    exit(1)


_LOGGER = logging.getLogger(__name__)


class DynamicToolbar(NavigationToolbar):

    def __init__(self, plotCanvas, parent):
        super().__init__(plotCanvas, parent)
        self.removeButton( 'Subplots' )

    def removeButton(self, buttonName):
        items = []
        for ii in self.toolitems:
            name = ii[0]
            if name is not None and name == buttonName:
                continue
            items.append(ii)
        self.toolitems = tuple( items )

        self.clear()            ## remove previous buttons
        #self._init_toolbar()    ## add current buttons

    def home(self, *args):
        super().home(*args)
        self._restore_view()

    def _restore_view(self):
        axesList = self._get_axes()
        for ax in axesList:
            ax.set_xlim(auto=True)
            ax.set_ylim(auto=True)
        self.canvas.draw_idle()

    def _get_axes(self):
        return self.canvas.figure.get_axes()

