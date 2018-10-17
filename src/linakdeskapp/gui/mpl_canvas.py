#
#
#

import logging

try:
    import matplotlib
    # Make sure that we are using QT5
    matplotlib.use('Qt5Agg')
    
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
except ImportError as e:
    ### No module named <name>
    logging.exception("Exception while importing")
    exit(1)

from .qt import QtCore, QtWidgets



_LOGGER = logging.getLogger(__name__)



class MplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent = None, width = 5, height = 4, dpi = 100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(1, 1, 1)
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def setBackgroundByRGB(self, r, g, b):
        rgbColor = ( r/255, g/255, b/255, 1.0 )
        self.fig.patch.set_facecolor( rgbColor )
        
    def setBackgroundByQColor(self, bgcolor):
        rgbColor = ( bgcolor.red()/255, bgcolor.green()/255, bgcolor.blue()/255, 1.0 )
        self.fig.patch.set_facecolor( rgbColor )
        ###_LOGGER.debug("setting background: %r", rgbColor)

    def drawFigure(self):
        pass
        
        
        
class DynamicMplCanvas(MplCanvas):
    """A canvas that updates itself every second with a new plot."""
 
    def __init__(self, *args, **kwargs):
        MplCanvas.__init__(self, *args, **kwargs)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._update)
        self.timer.start(1000)
        
    def update_figure(self):
        pass
 
    def _update(self):
        self.update_figure()
        self.drawFigure()

