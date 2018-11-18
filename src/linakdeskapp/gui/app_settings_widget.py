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
        self.positionTimer = QtCore.QTimer()
        self.positionTimer.timeout.connect( self._positionTimeout )
        self.positionTimer.setSingleShot(True)
        
        self._setStatusFromReminder()
    
        self.ui.enabledRemCB.stateChanged.connect( self._toggleReminder )
        self.ui.sitSB.valueChanged.connect( self._toggleSit )
        self.ui.standSB.valueChanged.connect( self._toggleStand )
        
        self.labelTimer = QtCore.QTimer()
        self.labelTimer.timeout.connect( self._refreshStateInfo )
        self.labelTimer.start(300)
        
        ## tray combo box
        self.ui.trayThemeCB.currentIndexChanged.connect( self._trayThemeChanged )
        for item in TrayIconTheme:
            itemName = item.name
            self.ui.trayThemeCB.addItem( itemName, item )
        
    def attachDevice(self, device):
        if self.device != None:
            ## disconnect old object
            self.device.positionChanged.disconnect( self._updatePositionState )
            
        self.device = device
        
        reminderActivated = self.reminder.isEnabled()
        self._setReminderState( reminderActivated )
        
        self.ui.positionChartWidget.attachDevice( device )
        
        ## connect new object
        if self.device != None:
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
        self._refreshStateInfo()
        if self.sitting == True:
            ## is sitting -- time to stand
            self.showMessage.emit("It's time to stand up")
        elif self.sitting == False:
            self.showMessage.emit("It's time to sit down")
        else:
            self.showMessage.emit("waiting for device")
        self.indicatePositionChange.emit(True)
            
    def _updatePositionState(self):
        deskHeight = self.device.currentPosition()
        devicePosition = self.isDevicePositionSitting(deskHeight)
        if self.sitting == devicePosition:
            ## position not changed
            return
        self._setPositionState(devicePosition)
    
    def _trayThemeChanged(self):
        selectedTheme = self.ui.trayThemeCB.currentData()
        self.iconThemeChanged.emit( selectedTheme )
    
    ## =================================================
    
    
    def _setReminderState(self, state):
        if self.device == None:
            self._disableWidget()
            return
        if state == False:
            self._stopPositionTimer()
            return
        deskHeight = self.device.currentPosition()
        devicePosition = self.isDevicePositionSitting(deskHeight)
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
        self._updateTotalTime()
        self.sitting = True
        if self.reminder.isEnabled() == False:
            self._stopPositionTimer()
            return
        timeout = self.reminder.sitTime * 1000 * 60
        self.positionTimer.start( timeout )
        self._refreshStateInfo()
        self.indicatePositionChange.emit(False)
        
    def _setStandingState(self):
        self._updateTotalTime()
        self.sitting = False
        if self.reminder.isEnabled() == False:
            self._stopPositionTimer()
            return
        timeout = self.reminder.standTime * 1000 * 60
        self.positionTimer.start( timeout )
        self._refreshStateInfo()
        self.indicatePositionChange.emit(False)

    def _stopPositionTimer(self):
        self.positionTimer.stop()
        self._refreshStateInfo()
        self.indicatePositionChange.emit(False)

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
        self._setCurrentTrayTheme( trayTheme )
        
        settings.endGroup()
        
        self._setStatusFromReminder()        
    
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
        
    def _setStatusFromReminder(self):
        reminderActivated = self.reminder.isEnabled()
        self.ui.enabledRemCB.setChecked( reminderActivated )
        self._setReminderState( reminderActivated )
        self.ui.sitSB.setValue( self.reminder.sitTime )
        self.ui.standSB.setValue( self.reminder.standTime )

    def _refreshStateInfo(self):
        stateInfo = self._getStateInfo()
        self.ui.remStatusLabel.setText( stateInfo )
        
        if self.device == None:
            return
        self._updateTotalTime()
        
        formattedSitTime = formatTimeDelta( self.totalSit )
        formattedStandTime = formatTimeDelta( self.totalStand )
        self.ui.totalSitLabel.setText( formattedSitTime )
        self.ui.totalStandLabel.setText( formattedStandTime )
        
        self.stateInfoChanged.emit( stateInfo )
    
    def _updateTotalTime(self):
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
    
    def _getStateInfo(self):
        if self.device == None:
            return "device disconnected"            
        if self.reminder.isEnabled() == False:
            return "stopped" 
        if self.positionTimer.isActive() == False:
            if self.sitting == True:
                return "waiting for stand up" 
            elif self.sitting == False:
                return "waiting for sit down"
            else:
                return "waiting for device"
        remaining = self.positionTimer.remainingTime()
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
    
    def _disableWidget(self):
        self.device = None
        self.sitting = None
        self.positionTime = None
        self._stopPositionTimer()
        
    