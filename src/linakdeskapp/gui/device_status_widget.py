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


from . import uiloader

from linakdeskapp.gui.device_connector import ConnectionState



UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )



class DeviceStatusWidget(QtBaseClass):
    def __init__(self, parentWidget = None):
        super().__init__(parentWidget)
        
        self.device = None
        
        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self._refreshWidget()
 
    def attachConnector(self, connector):
        if self.device != None:
            ## disconnect old object
            self.device.connectionStateChanged.disconnect( self._refreshWidget )
            self.device.settingChanged.disconnect( self._refreshWidget )
            self.device.positionChanged.disconnect( self._refreshPosition )
            self.device.speedChanged.disconnect( self._refreshSpeed )
            
        self.device = connector
        
        self._refreshWidget()
        
        if self.device != None:
            ## connect new object
            self.device.connectionStateChanged.connect( self._refreshWidget )
            self.device.settingChanged.connect( self._refreshWidget )
            self.device.positionChanged.connect( self._refreshPosition )
            self.device.speedChanged.connect( self._refreshSpeed )

    def _refreshWidget(self):
        status = self.getDeviceConnectionStatus()
        if status == ConnectionState.CONNECTED:
            self.ui.statusLabel.setText( "connected" )
            self.ui.deviceLabel.setText( self.device.name() )
            self.ui.deviceTypeLabel.setText( self.device.deviceType() )
            self.ui.userTypeLabel.setText( self.device.userType() )
            reminderSettings = self.device.reminderSettings()
            if reminderSettings != None:
                self.ui.reminderLabel.setText( reminderSettings.currentReminderInfo() )
            else:
                self.ui.reminderLabel.setText( "None" )
            self._refreshPosition()
            self._refreshSpeed()
            return
        
        if status == ConnectionState.CONN_IN_PROGRESS:
            self.ui.statusLabel.setText("connecting...")
        else:
            self.ui.statusLabel.setText("disconnected")

        ## clear rest
        self.ui.deviceLabel.setText("")
        self.ui.deviceTypeLabel.setText("")
        self.ui.userTypeLabel.setText("")
        self.ui.reminderLabel.setText("")
        self.ui.positionLabel.setText("")
        self.ui.speedLabel.setText("")
        
    def getDeviceConnectionStatus(self):
        if self.device == None:
            return ConnectionState.DISCONNECTED
        return self.device.getConnectionStatus()

    def _refreshPosition(self):
        self.ui.positionLabel.setText( self.device.positionCm() )
        
    def _refreshSpeed(self):
        currSpeed = self.device.currentSpeed()
        self.ui.speedLabel.setText( str(currSpeed) )
