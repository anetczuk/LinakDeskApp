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

from . import uiloader

from .qt import QPushButton
from .qt import clearLayout



UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )



class DeviceControlWidget(QtBaseClass):
    
    def __init__(self, parentWidget = None):
        super().__init__(parentWidget)
        
        self.device = None
        self.favButtons = list()
        
        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self.attachDevice(None)
        
        self.ui.upPB.pressed.connect(self._goingUp)
        self.ui.upPB.released.connect(self._stopMoving)
        self.ui.downPB.pressed.connect(self._goingDown)
        self.ui.downPB.released.connect(self._stopMoving)
        self.ui.stopPB.clicked.connect(self._stopMoving)
        self.ui.topPB.clicked.connect(self._goingTop)
        self.ui.bottomPB.clicked.connect(self._goingBottom)

    def attachDevice(self, device):
        if self.device != None:
            ## disconnect old object
            self.device.favoritiesChanged.disconnect( self._refreshFavLayout )
            
        self.ui.deviceStatus.attachDevice(device)
        self.device = device
        if self.device == None:
            self._refreshWidget(False)
            return
         
        self._refreshWidget(True)
            
        ## connect new object
        self.device.favoritiesChanged.connect( self._refreshFavLayout )

    def _refreshWidget(self, connected):
        if connected == False:
            self.ui.upPB.setEnabled(False)
            self.ui.downPB.setEnabled(False)
            self.ui.stopPB.setEnabled(False)
            self.ui.topPB.setEnabled(False)
            self.ui.bottomPB.setEnabled(False)
            self.ui.favLayout.setEnabled(False)
            self._clearFavLayout()
        else:
            self.ui.upPB.setEnabled(True)
            self.ui.downPB.setEnabled(True)
            self.ui.stopPB.setEnabled(True)
            self.ui.topPB.setEnabled(True)
            self.ui.bottomPB.setEnabled(True)
            self.ui.favLayout.setEnabled(True)
            self._genFavButtons()

    def _goingUp(self):
        if self.device == None:
            return
        self.device.moveUp()
    
    def _goingDown(self):
        if self.device == None:
            return
        self.device.moveDown()
    
    def _goingTop(self):
        if self.device == None:
            return
        self.device.moveToTop()
    
    def _goingBottom(self):
        if self.device == None:
            return
        self.device.moveToBottom()
        
    def _stopMoving(self):
        if self.device == None:
            return
        self.device.stopMoving()
    
    def _moveToFav(self, favIndex):
        if self.device == None:
            return
        self.device.moveToFav( favIndex )
        
    def _getFavList(self):
        if self.device == None:
            return []        
        return self.device.favValues()
        
    def _clearFavLayout(self):
        clearLayout( self.ui.favLayout )
        self.favButtons.clear()
            
    def _genFavButtons(self):
        self._clearFavLayout()
        
        favourities = self._getFavList()
        for i in range( len(favourities) ):
            fav = favourities[i]
            button = QPushButton(self)
            self._updateFavButton(button, fav)
            favHandler = functools.partial(self._moveToFav, i)
            button.clicked.connect( favHandler )
            self.ui.favLayout.addWidget( button )
            self.favButtons.append(button)
    
    def _refreshFavLayout(self, favIndex):
        self._refreshFavButton(favIndex)
        
    def _refreshFavButton(self, favIndex):
        favourities = self._getFavList()
        if favIndex >= len(favourities):
            return 
        favValue = favourities[ favIndex ]
        button = self.favButtons[ favIndex ]
        self._updateFavButton(button, favValue)
    
    def _updateFavButton(self, button, favValue):
        label = str( favValue )
        button.setText( label )
        if favValue != None:
            button.setEnabled( True )
        else:
            button.setEnabled( False )
    
        