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
import time

from . import uiloader
from .qt import QtCore
from .qt import pyqtSignal
from .tray_icon import TrayIconTheme


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
    
    showMessage             = pyqtSignal(str)
    stateInfoChanged        = pyqtSignal(str)
    indicatePositionChange  = pyqtSignal(bool)
    iconThemeChanged        = pyqtSignal( TrayIconTheme )
    
    
    def __init__(self, parentWidget = None):
        super().__init__(parentWidget)

        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self.device = None
        
        self.reminder = Reminder()
        self.sitting = None             ## current position, boolean. None means unknown
        self.positionTime = None
        
        self.totalSit = datetime.timedelta()
        self.totalStand = datetime.timedelta()

        ## timer reminds to change position after given amount of time
        self.reminderTimer = QtCore.QTimer()
        self.reminderTimer.timeout.connect( self._reminderTimeout )
        self.reminderTimer.setSingleShot(True)
    
        self.ui.enabledRemCB.stateChanged.connect( self._toggleReminder )
        self.ui.sitSB.valueChanged.connect( self._toggleSitValue )
        self.ui.standSB.valueChanged.connect( self._toggleStandValue )
        
        self.labelTimer = QtCore.QTimer()
        self.labelTimer.timeout.connect( self._updateStateInfo )
        self.labelTimer.setInterval(300)
        
        ## tray combo box
        self.ui.trayThemeCB.currentIndexChanged.connect( self._trayThemeChanged )
        for item in TrayIconTheme:
            itemName = item.name
            self.ui.trayThemeCB.addItem( itemName, item )
            
        self._disableWidget()
        
    def attachDevice(self, device):
        if self.device != None:
            ## disconnect old object
            self.device.positionChanged.disconnect( self._updatePositionState )
            
        self.device = device
        
        if self.device != None:
            self._enableWidget()
        else:
            self._disableWidget()
            
        self.ui.positionChartWidget.attachDevice( device )
        
        ## connect new object
        if self.device != None:
            self.device.positionChanged.connect( self._updatePositionState )


    ## ================= slots ========================


    def _trayThemeChanged(self):
        selectedTheme = self.ui.trayThemeCB.currentData()
        self.iconThemeChanged.emit( selectedTheme )
        
    ## turn reminder on / off
    def _toggleReminder(self, state):
        ## state: 0 -- unchecked
        ## state: 2 -- checked
        enabled = (state != 0)
        self.reminder.setEnabled( enabled )
        self._setReminderTimer( enabled )       ## toggle reminder by checkbox
        self._displayStateInfo()
    
    ## sitting spin button changed
    def _toggleSitValue(self, value):
        self.reminder.sitTime = value
        if self.sitting == True:
            self._setReminderTimeout()                  ## spin values changed
            self.indicatePositionChange.emit(False)
    
    ## standing spin button changed
    def _toggleStandValue(self,  value):
        self.reminder.standTime = value
        if self.sitting == False:
            self._setReminderTimeout()                  ## spin values changed
            self.indicatePositionChange.emit(False)
    
    def _reminderTimeout(self):
        self._displayStateInfo()
        
        if self.device == None:
            _LOGGER.debug("device not attached -- do nothing")
            return
        _LOGGER.debug("reminder timer timeout handler")
        
        if self.sitting == True:
            ## is sitting -- time to stand
            self.showMessage.emit("It's time to stand up")
        elif self.sitting == False:
            self.showMessage.emit("It's time to sit down")
        else:
            self.showMessage.emit("waiting for device")
        self.indicatePositionChange.emit(True)
    
    ## triggered when total time timer ticks
    def _updateStateInfo(self):
        self._updateTotalTime()         ## update total timers after timer tick
        self._displayStateInfo()
    
    ## triggered when desk is moving
    def _updatePositionState(self):
        deskHeight = self.device.currentPosition()
        devicePosition = self.isDevicePositionSitting(deskHeight)
        if self.sitting == devicePosition:
            ## position not changed
            return
        self._updateTotalTime()         ## update previous state time
        self.sitting = devicePosition
        self._displayStateInfo()
        if self.reminder.isEnabled() == False:
            return
        self._setReminderTimeout()                  ## position has changed
        self.reminderTimer.start()
        self.indicatePositionChange.emit(False)

    
    ## =================================================
    

    def _enableWidget(self):
        self._updatePositionState()
        self.labelTimer.start()
        
    def _disableWidget(self):
        self.sitting = None
        self.positionTime = None
        self._setReminderTimer( False )                     ## disabling widget -- disable timer
        self.labelTimer.stop()
        self._displayStateInfo()

    def loadSettings(self, settings):
        self.ui.positionChartWidget.loadSettings( settings )
        
        settings.beginGroup( self.objectName() )
        
        enabled = settings.value("enabled", True, type=bool)
        self.reminder.setEnabled( enabled )
        
        self.reminder.sitTime = settings.value("sitTime", 55, type=int)
        self.reminder.standTime = settings.value("standTime", 5, type=int)
        
        sitTotalTime = settings.value("sitTotalTime", 0, type=float)
        standTotalTime = settings.value("standTotalTime", 0, type=float)
        self.totalSit += datetime.timedelta(seconds = sitTotalTime)
        self.totalStand += datetime.timedelta(seconds = standTotalTime)
        
        trayTheme = settings.value("trayIcon", None, type=str)
        
        settings.endGroup()
        
        ## update reminder
        self._setCurrentTrayTheme( trayTheme )
        reminderActivated = self.reminder.isEnabled()
        self.ui.enabledRemCB.setChecked( reminderActivated )
        self.ui.sitSB.setValue( self.reminder.sitTime )
        self.ui.standSB.setValue( self.reminder.standTime )
        self._displayStateInfo()
    
    def _setCurrentTrayTheme( self, trayTheme: str ):
        themeIndex = TrayIconTheme.indexOf( trayTheme )
        if themeIndex < 0:
            _LOGGER.warn("could not find index for theme: %r", trayTheme)
            return
        self.ui.trayThemeCB.setCurrentIndex( themeIndex )
    
    def saveSettings(self, settings):
        self.ui.positionChartWidget.saveSettings( settings )
        
        settings.beginGroup( self.objectName() )
        settings.setValue("enabled", self.reminder.enabled)
        settings.setValue("sitTime", self.reminder.sitTime)
        settings.setValue("standTime", self.reminder.standTime)
        
        settings.setValue("sitTotalTime", self.totalSit.total_seconds())
        settings.setValue("standTotalTime", self.totalStand.total_seconds())
        
        selectedTheme = self.ui.trayThemeCB.currentData()
        settings.setValue("trayIcon", selectedTheme.name)
        
        settings.endGroup()

    
    ## might be toggled by user in anytime
    def _setReminderTimer(self, enable):
        if enable == False:
            ## disable reminder
            self.reminderTimer.stop()
            self.indicatePositionChange.emit(False)
            return
        if self.sitting != None:
            ## enable reminder
            self._setReminderTimeout()          ## enabling timer
            self.reminderTimer.start()
    
    def _setReminderTimeout(self):
        if self.sitting == None:
            return
        if self.sitting == True:
            ## started sitting
            _LOGGER.debug("sitting started")
            timeout = self.reminder.sitTime * 1000 * 60
            self.reminderTimer.setInterval( timeout )
        else:
            ## started standing
            _LOGGER.debug("standing started")
            timeout = self.reminder.standTime * 1000 * 60
            self.reminderTimer.setInterval( timeout )
    
    def _updateTotalTime(self):
        if self.device == None:
            return
        if self.sitting == None:
            return
        if self.positionTime == None:
            self.positionTime = time.time()
            return
        curr = time.time()
        diff = curr - self.positionTime
        passedTime = datetime.timedelta(seconds = diff)
        self.positionTime = curr
        if self.sitting == True:
            self.totalSit += passedTime
        else:
            self.totalStand += passedTime
    
    def _displayStateInfo(self):
        stateInfo = self._getStateInfo()
        self.ui.remStatusLabel.setText( stateInfo )
        
        formattedSitTime = formatTimeDelta( self.totalSit )
        formattedStandTime = formatTimeDelta( self.totalStand )
        self.ui.totalSitLabel.setText( formattedSitTime )
        self.ui.totalStandLabel.setText( formattedStandTime )
        
        self.stateInfoChanged.emit( stateInfo )
    
    def _getStateInfo(self):
        if self.device == None:
            return "device disconnected"            
        if self.reminder.isEnabled() == False:
            return "stopped" 
        if self.reminderTimer.isActive() == False:
            ## reminder timed out
            if self.sitting == True:
                return "waiting for stand up" 
            elif self.sitting == False:
                return "waiting for sit down"
            else:
                return "waiting for device"
        remaining = self.reminderTimer.remainingTime()
        remainingTime = datetime.timedelta(milliseconds=remaining)
        formattedTime = formatTimeDelta( remainingTime )
        if self.sitting == True:
            return "sitting countdown: " + formattedTime
        elif self.sitting == False:
            return "standing countdown: " + formattedTime
        else:
            return "waiting for device"
    
    def isDevicePositionSitting(self, deskHeight):
        if deskHeight < self.STAND_HEIGHT:
            ## sitting
            return True
        else:
            ## standing
            return False
    