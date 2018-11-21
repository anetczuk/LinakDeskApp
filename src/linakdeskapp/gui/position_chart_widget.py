# MIT License
# 
# Copyright (c) 2017 Arkadiusz Netczuk <dev.arnet@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
 
 
import logging

from . import uiloader

from .mpl.mpl_toolbar import DynamicToolbar



_LOGGER = logging.getLogger(__name__)


UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )



class PositionChartWidget(QtBaseClass):
    
    def __init__(self, parentWidget = None):
        super().__init__(parentWidget)

        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self.device = None
        enabledChart = True
    
        bgcolor = parentWidget.palette().color(parentWidget.backgroundRole())
        self.ui.positionChart.setBackgroundByQColor( bgcolor )
    
        self.ui.enabledCB.setChecked( enabledChart )
        self.ui.enabledCB.stateChanged.connect( self._toggleEnabled )
        
        self.toolbar = DynamicToolbar(self.ui.positionChart, self)
        self.ui.toolbarLayout.addWidget( self.toolbar )
        
        self._refreshWidget()

    
    def attachConnector(self, connector):
        if self.device != None:
            ## disconnect old object
            self.device.newConnection.disconnect( self._refreshWidget )
            self.device.disconnected.disconnect( self._refreshWidget )
            self.device.positionChanged.disconnect( self._updatePositionState )
            
        self.device = connector
        
        self._refreshWidget()
        
        if self.device != None:
            ## connect new object
            self.device.newConnection.connect( self._refreshWidget )
            self.device.disconnected.connect( self._refreshWidget )
            self.device.positionChanged.connect( self._updatePositionState )
        
    def loadSettings(self, settings):
        settings.beginGroup( self.objectName() )
        enabled = settings.value("chart_enabled", True, type=bool)
        settings.endGroup()
         
        self.ui.enabledCB.setChecked( enabled )
    
    def saveSettings(self, settings):
        settings.beginGroup( self.objectName() )
        enabledChart = self.ui.enabledCB.isChecked()
        settings.setValue("chart_enabled", enabledChart)
        settings.endGroup()
        
    def _refreshWidget(self):
        ## _LOGGER.info("setting enabled: %s", enabled)
        connected = self.isDeviceConnected()
        if connected == True:
            enabledChart = self.ui.enabledCB.isChecked()
            self.toolbar.setEnabled( enabledChart )
            self.ui.positionChart.setEnabled( enabledChart )
            self._updatePositionState()         ## add current position
        else:
            self.toolbar.setEnabled( False )
            self.ui.positionChart.setEnabled( False )
        
    def isDeviceConnected(self):
        if self.device == None:
            return False
        return self.device.isConnected()

    def _updatePositionState(self):
        enabledChart = self.ui.enabledCB.isChecked()
        if enabledChart == False:
            return
        deskHeight = self.device.currentPosition()
        self.ui.positionChart.addData( deskHeight )
    
    def _toggleEnabled(self, state):
        ## state: 0 -- unchecked
        ## state: 2 -- checked
        self._refreshWidget()
        