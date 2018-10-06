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

from .qt import QPushButton, QSpinBox, QCheckBox, QHBoxLayout
from .qt import clearLayout



_LOGGER = logging.getLogger(__name__)


UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )



class DeviceSettingsWidget(QtBaseClass):
    def __init__(self, parentWidget = None):
        super().__init__(parentWidget)
        
        self.device = None
        
        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self.attachDevice(self.device)
        
        self.ui.refreshPB.pressed.connect(self._refreshSettings)
        self.ui.remUpdatePB.pressed.connect(self._updateReminderSettings)
 
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
        self._refreshReminderWidget(connected)
        self._refreshFavoritiesWidget(connected)
        
    def _refreshReminderWidget(self, connected):
        if connected == False:
            self.ui.refreshPB.setEnabled(False)
            self.ui.capsLabel.setText("")
            self.ui.counterLabel.setText("")
            self._clearReminderFlagsLayout()
            self._clearReminderLayout()
            self.ui.remUpdatePB.setEnabled(False)
        else:
            self.ui.refreshPB.setEnabled(True)
            self.ui.capsLabel.setText( self.device.capabilities() )
            reminderSettings = self.device.reminderSettings()
            self.ui.counterLabel.setText( str( reminderSettings.counter() ) )
            self.ui.reminderStateLabel.setText( reminderSettings.state() )
            self._genReminderFlagsButtons()
            self._genReminderWidgets()
            self.ui.remUpdatePB.setEnabled(True)

    def _refreshSettings(self):
        self.device.readReminderState()

    def _updateReminderSettings(self):
        self.device.sendReminderState()
        self.device.readReminderState()

    def _getReminderList(self):
        if self.device == None:
            return []        
        return self.device.reminderValues()
        
    def _clearReminderFlagsLayout(self):
        clearLayout(self.ui.reminderFlagsLayout)
            
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
        clearLayout(self.ui.reminderLayout)
        clearLayout(self.ui.remSpinLayout)
            
    def _genReminderWidgets(self):
        self._clearReminderLayout()
        
        reminderSettings = self.device.reminderSettings()
        reminders = reminderSettings.getRemindersList()
        currReminder = reminderSettings.getReminderIndex()
        
        for i in range(0, len(reminders)):
            rem = reminders[i]
            remIndex = i+1
            
            button = QPushButton(self)
            ##button.setText("R" + str(remIndex))
            button.setText( rem.info() )
            if remIndex == currReminder:
                button.setStyleSheet("font: bold;")
            favHandler = functools.partial(self._toggleReminder, remIndex)
            button.clicked.connect( favHandler )
            self.ui.reminderLayout.addWidget( button )
            
            spin = QSpinBox(self)
            spin.setValue( rem.sit )
            spin.setMinimum(1)
            spin.setMaximum(255)
            favHandler = functools.partial(self._toggleSit, remIndex)
            spin.valueChanged.connect( favHandler )
            self.ui.remSpinLayout.addWidget( spin )
 
            spin = QSpinBox(self)
            spin.setValue( rem.stand )
            spin.setMinimum(1)
            spin.setMaximum(255)
            favHandler = functools.partial(self._toggleStand, remIndex)
            spin.valueChanged.connect( favHandler )
            self.ui.remSpinLayout.addWidget( spin )

    def _toggleReminder(self, remIndex):
        reminderSettings = self.device.reminderSettings()
        reminderSettings.switchReminder(remIndex)
        self.device.sendReminderState()
        self.device.readReminderState()
        
    def _toggleSit(self, remIndex, value):
        reminderSettings = self.device.reminderSettings()
        currReminder = reminderSettings.getReminderByIndex(remIndex)
        currReminder.sit = value
        
    def _toggleStand(self, remIndex, value):
        reminderSettings = self.device.reminderSettings()
        currReminder = reminderSettings.getReminderByIndex(remIndex)
        currReminder.stand = value


    # =============================================================


    def _refreshFavoritiesWidget(self, connected):
        if connected == False:
            self._clearFavLayout()
        else:
            self._genFavButtons()

    def _clearFavLayout(self):
        clearLayout(self.ui.favLayout)

    def _genFavButtons(self):
        self._clearFavLayout()
        
        self.favSpinBoxes = []
        self.favGoToButtons = []
        
        favorities = self.device.favPositions()
        #_LOGGER.info("got favs: %s", favorities)
        for i in range( len(favorities) ):
            fav = favorities[i]
            hLayout = self._genFavHLayout( i, fav )
            self.ui.favLayout.addLayout( hLayout )
    
    def _genFavHLayout(self, favIndex, favValue):
        layout = QHBoxLayout()

        check = QCheckBox(self)
        if favValue != None:
            check.setChecked(True)
        else:
            check.setChecked(False)
        favHandler = functools.partial(self._toggleFavEnable, favIndex)
        check.stateChanged.connect( favHandler )
        layout.addWidget( check )
        
        layout.addSpacing( 6 )
                    
        spin = QSpinBox(self)
        spin.setMinimum(1)
        spin.setMaximum(255)
        if favValue != None:
            spin.setEnabled(True)
            spin.setValue( favValue )
        else:
            spin.setEnabled(False)
            currPos = self.device.currentPosition()
            spin.setValue( currPos )
        favHandler = functools.partial(self._toggleFav, favIndex)
        spin.valueChanged.connect( favHandler )
        layout.addWidget( spin )
        self.favSpinBoxes.append( spin )
        
        layout.addSpacing( 6 )
        
        button = QPushButton("Go To", self)
        if favValue == None:
            button.setEnabled( False )
        favHandler = functools.partial(self._moveToFav, favIndex)
        button.clicked.connect( favHandler )
        layout.addWidget( button )
        self.favGoToButtons.append( button )
        
        layout.addSpacing( 6 )

        button = QPushButton("Update", self)
        favHandler = functools.partial(self._updateFavorite, favIndex)
        button.clicked.connect( favHandler )
        layout.addWidget( button )
        
        layout.addStretch(1)
        
        return layout

    def _toggleFavEnable(self, favIndex, state):
        ## state: 0 -- unchecked
        ## state: 2 -- checked
        if state == 0:
            ## unchecked
            self.device.setFavPosition(favIndex, None)
            self.favGoToButtons[favIndex].setEnabled(False)
            self.favSpinBoxes[favIndex].setEnabled(False)
        else:
            ## checked
            value = self.favSpinBoxes[favIndex].value()
            self.device.setFavPosition(favIndex, value)
            self.favGoToButtons[favIndex].setEnabled(True)
            self.favSpinBoxes[favIndex].setEnabled(True)
    
    def _toggleFav(self, favIndex, value):
        self.device.setFavPosition( favIndex, value )
        
    def _moveToFav(self, favIndex):
        self.device.moveToFav( favIndex )
        
    def _updateFavorite(self, favIndex):
        self.device.sendFavoriteState( favIndex )
    