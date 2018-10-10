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

from .qt import QtCore


_LOGGER = logging.getLogger(__name__)


UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )



class Reminder():
    def __init__(self):
        self.enabled = False
        self.sitTime = 55
        self.standTime = 5
        
    def isEnabled(self):
        return self.enabled
    
    def setEnabled(self, state):
        self.enabled = state
        
        

class AppSettingsWidget(QtBaseClass):
    
    STAND_HEIGHT = 96
    
    
    def __init__(self, parentWidget = None):
        super().__init__(parentWidget)

        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self.trayIcon = None
        self.device = None
        
        self.reminder = Reminder()
        self.sitting = True             ## current position

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect( self._timerHandler )
        
        self._setStatusFromReminder()
    
        self.ui.enabledRemCB.stateChanged.connect( self._toggleReminder )
        self.ui.sitSB.valueChanged.connect( self._toggleSit )
        self.ui.standSB.valueChanged.connect( self._toggleStand )
        
    def attachTray(self, trayIcon):
        self.trayIcon = trayIcon
        
    def attachDevice(self, device):
        if self.device != None:
            ## disconnect old object
            self.device.positionChanged.disconnect( self._refreshHeight )
            
        self.device = device
        
        ## connect new object
        self.device.positionChanged.connect( self._refreshHeight )

    def _toggleReminder(self, state):
        ## state: 0 -- unchecked
        ## state: 2 -- checked
        enabled = (state != 0)
        self.reminder.setEnabled( enabled )
        self._setSittingTimer()
    
    def _setSittingTimer(self):
        self.sitting = True
        if self.reminder.isEnabled() == False:
            self.ui.remStatusLabel.setText( "Stopped" )
            self.timer.stop()
            return
        self.ui.remStatusLabel.setText( "Sitting countdown" )
        timeout = self.reminder.sitTime * 1000 * 60
        self.timer.start( timeout )
        _LOGGER.debug( "setting sitting timer, timeout: %s", str(self.reminder.sitTime) )
        
    def _setStandingTimer(self):
        self.sitting = False
        if self.reminder.isEnabled() == False:
            self.ui.remStatusLabel.setText( "Stopped" )
            self.timer.stop()
            return
        self.ui.remStatusLabel.setText( "Standing countdown" )
        timeout = self.reminder.standTime * 1000 * 60
        self.timer.start( timeout )
        _LOGGER.debug( "setting standing timer, timeout: %s", str(self.reminder.standTime) )
    
    def _toggleSit(self, value):
        self.reminder.sitTime = value
        self._setSittingTimer()
        
    def _toggleStand(self,  value):
        self.reminder.standTime = value
    
    def _timerHandler(self):
        _LOGGER.debug("timer timeout handler")
        self.ui.remStatusLabel.setText( "Waiting for change of position" )
        if self.sitting == True:
            ## is sitting -- time to stand
            self._showMessage("It's time to stand up")
        else:
            self._showMessage("It's time to sit down")

    def _showMessage(self, message):
        if self.trayIcon == None:
            return
        self.trayIcon.showMessage("Desk", message)
    
    def _refreshHeight(self):
        deskHeight = self.device.currentPosition()
        if deskHeight >= self.STAND_HEIGHT:
            self._movedToStanding()
            ## started standing
        else:
            ## started sitting
            self._movedToSitting()
    
    def _movedToStanding(self):
        if self.sitting != True:
            return
        self._setStandingTimer()
    
    def _movedToSitting(self):
        if self.sitting != False:
            return
        self._setSittingTimer()
        
    def _setStatusFromReminder(self):
        reminderActivated = self.reminder.isEnabled()
        self.ui.enabledRemCB.setChecked( reminderActivated )
        self._setSittingTimer()
        
        self.ui.sitSB.setValue( self.reminder.sitTime )
        self.ui.standSB.setValue( self.reminder.standTime )
        
    def loadSettings(self, settings):
        settings.beginGroup( self.objectName() )
        self.reminder.enabled = bool( settings.value("enabled", False) )
        self.reminder.sitTime = int( settings.value("sitTime", 55) )
        self.reminder.standTime = int( settings.value("standTime", 5) )
        settings.endGroup()
        self._setStatusFromReminder()
    
    def saveSettings(self, settings):
        settings.beginGroup( self.objectName() )
        settings.setValue("enabled", self.reminder.enabled)
        settings.setValue("sitTime", self.reminder.sitTime)
        settings.setValue("standTime", self.reminder.standTime)
        settings.endGroup()
    
    