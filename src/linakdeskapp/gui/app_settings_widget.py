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
import datetime

from . import uiloader

from .qt import QtCore


_LOGGER = logging.getLogger(__name__)


UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )



def formatTimeDelta(timeDelta):
    ret = ""
    seconds = int( timeDelta.seconds % 60 )
    minutes = int( timeDelta.seconds / 60 % 60 )
    hours   = int( timeDelta.seconds / 3600 )
    if timeDelta.days > 0:
        ret += timeDelta.days + ","
    if hours > 0:
        ret += "%02d:" % (hours)
    ret += "%02d:%02d" % (minutes, seconds)
    return ret
    
    
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

        self.positionTimer = QtCore.QTimer()
        self.positionTimer.timeout.connect( self._positionTimeout )
        self.positionTimer.setSingleShot(True)

        self.labelTimer = QtCore.QTimer()
        self.labelTimer.timeout.connect( self._refreshStateLabel )
        
        self._setStatusFromReminder()
    
        self.ui.enabledRemCB.stateChanged.connect( self._toggleReminder )
        self.ui.sitSB.valueChanged.connect( self._toggleSit )
        self.ui.standSB.valueChanged.connect( self._toggleStand )
        
    def attachTray(self, trayIcon):
        self.trayIcon = trayIcon
        
    def attachDevice(self, device):
        if self.device != None:
            ## disconnect old object
            self.device.positionChanged.disconnect( self._updatePositionState )
            
        self.device = device
        
        reminderActivated = self.reminder.isEnabled()
        self._setReminderState( reminderActivated )
        
        ## connect new object
        self.device.positionChanged.connect( self._updatePositionState )


    ## ================= slots ========================


    def _toggleReminder(self, state):
        ## state: 0 -- unchecked
        ## state: 2 -- checked
        enabled = (state != 0)
        self.reminder.setEnabled( enabled )
        self._setReminderState( enabled )
    
    def _toggleSit(self, value):
        self.reminder.sitTime = value
        if self.sitting == True:
            self._setSittingState()
        
    def _toggleStand(self,  value):
        self.reminder.standTime = value
        if self.sitting == False:
            self._setStandingState()

    def _positionTimeout(self):
        _LOGGER.debug("position timer timeout handler")
        self._refreshStateLabel()
        if self.sitting == True:
            ## is sitting -- time to stand
            self._showMessage("It's time to stand up")
        else:
            self._showMessage("It's time to sit down")
            
    def _updatePositionState(self):
        devicePosition = self.readDevicePosition()
        if self.sitting == devicePosition:
            ## position not changed
            return
        self._setPositionState(devicePosition)
    
    
    ## =================================================
    
    
    def _setReminderState(self, state):
        if state == False:
            self._stopPositionTimer()
            return
        if self.device == None:
            self._stopPositionTimer()
            return
        devicePosition = self.readDevicePosition()
        self._setPositionState(devicePosition)
        
    def _setPositionState(self, isSitting):
        if isSitting == False:
            ## started standing
            _LOGGER.debug("standing started")
            self._setStandingState()
        else:
            ## started sitting
            _LOGGER.debug("sitting started")
            self._setSittingState()
                
    def _setSittingState(self):
        self.sitting = True
        if self.reminder.isEnabled() == False:
            self._stopPositionTimer()
            return
        timeout = self.reminder.sitTime * 1000 * 60
        self.positionTimer.start( timeout )
        self._refreshStateLabel()
        
    def _setStandingState(self):
        self.sitting = False
        if self.reminder.isEnabled() == False:
            self._stopPositionTimer()
            return
        timeout = self.reminder.standTime * 1000 * 60
        self.positionTimer.start( timeout )
        self._refreshStateLabel()

    def _stopPositionTimer(self):
        self.positionTimer.stop()
        self._refreshStateLabel()

    def loadSettings(self, settings):
        settings.beginGroup( self.objectName() )
        enabled = bool( settings.value("enabled", False) )
        self.reminder.setEnabled( enabled )
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
        
    def _setStatusFromReminder(self):
        reminderActivated = self.reminder.isEnabled()
        self.ui.enabledRemCB.setChecked( reminderActivated )
        self._setReminderState( reminderActivated )
        self.ui.sitSB.setValue( self.reminder.sitTime )
        self.ui.standSB.setValue( self.reminder.standTime )

    def _refreshStateLabel(self):
        if self.device == None:
            self.ui.remStatusLabel.setText( "Device disconnected" )
            return            
        if self.reminder.isEnabled() == False:
            self.ui.remStatusLabel.setText( "Stopped" )
            return
        if self.positionTimer.isActive() == False:
            self.ui.remStatusLabel.setText( "Waiting for change of position" )
            return
        remaining = self.positionTimer.remainingTime()
        remainingTime = datetime.timedelta(milliseconds=remaining)
        formattedTime = formatTimeDelta( remainingTime )
        if self.sitting == True:
            self.ui.remStatusLabel.setText( "Sitting countdown: " + formattedTime )
        else:
            self.ui.remStatusLabel.setText( "Standing countdown: " + formattedTime )
        
    def _showMessage(self, message):
        if self.trayIcon == None:
            return
        self.trayIcon.showMessage("Desk", message)
    
    def readDevicePosition(self):
        deskHeight = self.device.currentPosition()
        if deskHeight < self.STAND_HEIGHT:
            ## sitting
            return True
        else:
            ## standing
            return False
    
    
    ## ========================================================
    
    
    def showEvent(self, event):
        self._refreshStateLabel()
        self.labelTimer.start(300)
    
    def hideEvent(self, event):
        self.labelTimer.stop()
    