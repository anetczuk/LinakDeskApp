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


import functools
import logging

from . import uiloader

from .qt import QPushButton



_LOGGER = logging.getLogger(__name__)


UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )



class DeviceSettingsWidget(QtBaseClass):
    def __init__(self, parentWidget = None):
        super().__init__(parentWidget)
        
        self.device = None
        
        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self.attachDevice(self.device)
 
    def attachDevice(self, device):
        if self.device != None:
            ## disconnect old object
            self.device.settingChanged.disconnect( self._refreshContent )
            
        self.device = device
        if self.device == None:
            self._refreshWidget(False)
            return
         
        self._refreshWidget(True)
        
        ## connect new object
        self.device.settingChanged.connect( self._refreshContent )
 
    def _refreshContent(self):
        self._refreshWidget(True)
 
    def _refreshWidget(self, connected):
        if connected == False:
            self._clearReminderFlagsLayout()
            self._clearReminderLayout()
#             self.ui.statusLabel.setText("disconnected")
#             self.ui.deviceLabel.setText("")
#             self.ui.deviceTypeLabel.setText("")
#             self.ui.capsLabel.setText("")
#             self.ui.userTypeLabel.setText("")
#             self.ui.reminderLabel.setText("")
#             self.ui.positionLabel.setText("")
#             self.ui.speedLabel.setText("")
#             self.ui.favsNumLabel.setText("")
        else:
            self._genReminderFlagsButtons()
            self._genReminderButtons()
#             self.ui.statusLabel.setText( "connected" )
#             self.ui.deviceLabel.setText( self.device.name() )
#             self.ui.deviceTypeLabel.setText( self.device.deviceType() )
#             self.ui.capsLabel.setText( self.device.capabilities() )
#             self.ui.userTypeLabel.setText( self.device.userType() )
#             self.ui.reminderLabel.setText( self.device.reminder() )
#             self._refreshPosition()
#             self._refreshSpeed()
#             self.ui.favsNumLabel.setText( str( self.device.favSlotsNumber() ) )

    def _getReminderList(self):
        if self.device == None:
            return []        
        return self.device.reminderValues()
        
    def _clearReminderFlagsLayout(self):
        for i in reversed(range(self.ui.reminderFlagsLayout.count())): 
            self.ui.reminderFlagsLayout.itemAt(i).widget().deleteLater()
            
    def _genReminderFlagsButtons(self):
        self._clearReminderFlagsLayout()
        
        reminderSettings = self.device.reminderSettings()
        
        button = QPushButton(self)
        favHandler = None
        if reminderSettings.getLights() == True:
            button.setText("Lights On")
            favHandler = functools.partial(self._toggleLights, False)
        else:
            button.setText("Lights Off")
            favHandler = functools.partial(self._toggleLights, True)
        button.clicked.connect( favHandler )
        self.ui.reminderFlagsLayout.addWidget( button )
        
        button = QPushButton(self)
        favHandler = None
        if reminderSettings.getWake() == True:
            button.setText("Wake On")
            favHandler = functools.partial(self._toggleWake, False)
        else:
            button.setText("Wake Off")
            favHandler = functools.partial(self._toggleWake, True)
        button.clicked.connect( favHandler )
        self.ui.reminderFlagsLayout.addWidget( button )
        
        button = QPushButton(self)
        favHandler = None
        if reminderSettings.getAutomaticDown() == True:
            button.setText("AutoDown On")
            favHandler = functools.partial(self._toggleAutoDown, False)
        else:
            button.setText("AutoDown Off")
            favHandler = functools.partial(self._toggleAutoDown, True)
        button.clicked.connect( favHandler )
        self.ui.reminderFlagsLayout.addWidget( button )
        
        button = QPushButton(self)
        favHandler = None
        if reminderSettings.getAutomaticUp() == True:
            button.setText("AutoUp On")
            favHandler = functools.partial(self._toggleAutoUp, False)
        else:
            button.setText("AutoUp Off")
            favHandler = functools.partial(self._toggleAutoUp, True)
        button.clicked.connect( favHandler )
        self.ui.reminderFlagsLayout.addWidget( button )
        
        button = QPushButton(self)
        favHandler = None
        if reminderSettings.getCmUnit() == True:
            button.setText("Cm unit")
            favHandler = functools.partial(self._toggleCmUnit, False)
        else:
            button.setText("Inch unit")
            favHandler = functools.partial(self._toggleCmUnit, True)
        button.clicked.connect( favHandler )
        self.ui.reminderFlagsLayout.addWidget( button )

    def _toggleLights(self, newState):
        reminderSettings = self.device.reminderSettings()
        reminderSettings.setLights(newState)
        self.device.sendReminderState()
        self.device.readReminderState()

    def _toggleWake(self, newState):
        reminderSettings = self.device.reminderSettings()
        reminderSettings.setWake(newState)
        self.device.sendReminderState()
        self.device.readReminderState()
        
    def _toggleAutoUp(self, newState):
        reminderSettings = self.device.reminderSettings()
        reminderSettings.setAutomaticUp(newState)
        self.device.sendReminderState()
        self.device.readReminderState()
        
    def _toggleAutoDown(self, newState):
        reminderSettings = self.device.reminderSettings()
        reminderSettings.setAutomaticDown(newState)
        self.device.sendReminderState()
        self.device.readReminderState()
        
    def _toggleCmUnit(self, newState):
        reminderSettings = self.device.reminderSettings()
        reminderSettings.setCmUnit(newState)
        self.device.sendReminderState()
        self.device.readReminderState()
    
    def _clearReminderLayout(self):
        for i in reversed(range(self.ui.reminderLayout.count())): 
            self.ui.reminderLayout.itemAt(i).widget().deleteLater()
            
    def _genReminderButtons(self):
        self._clearReminderLayout()
        
        reminderSettings = self.device.reminderSettings()
        reminders = reminderSettings.getRemindersList()
        currReminder = reminderSettings.getReminder()
        
        for i in range(0, len(reminders)):
            remIndex = i+1
            button = QPushButton(self)
            button.setText("R" + str(remIndex))
            if remIndex == currReminder:
                button.setStyleSheet("font: bold;")
            favHandler = functools.partial(self._toggleReminder, remIndex)
            button.clicked.connect( favHandler )
            self.ui.reminderLayout.addWidget( button )

    def _toggleReminder(self, remIndex):
        reminderSettings = self.device.reminderSettings()
        reminderSettings.switchReminder(remIndex)
        self.device.sendReminderState()
        self.device.readReminderState()
        
        