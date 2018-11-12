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
import functools

# from .qt import QtCore
from .qt import qApp, QSystemTrayIcon, QMenu, QAction
from .qt import QIcon

from . import resources



_LOGGER = logging.getLogger(__name__)



class TrayIcon(QSystemTrayIcon):
    def __init__(self, parent):
        super().__init__(parent)

        ## print("is tray available:",  QSystemTrayIcon.isSystemTrayAvailable() )

        self.device = None
        self.neutralIcon = None
        self.indicatorIcon = None
        self.currIconState = 0

        neutralPath = resources.getImagePath('office-chair_gray.png')
        indicatorPath = resources.getImagePath('office-chair-red_gray.png')
        self.setIconNeutral( QIcon( neutralPath ) )
        self.setIconIndicator( QIcon( indicatorPath ) )
        self.setNeutral()

        self.activated.connect( self._icon_activated )

        '''
            Define and add steps to work with the system tray icon
            show - show window
            hide - hide window
            exit - exit from application
        '''
        ##show_action = QAction("Show", self)
        ##hide_action = QAction("Hide", self)
        self.toggle_window_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        ##show_action.triggered.connect( parent.show )
        ##hide_action.triggered.connect( parent.hide )
        self.toggle_window_action.triggered.connect( self._toggleParent )
        quit_action.triggered.connect( qApp.quit )
        ##tray_menu.addAction( show_action )
        ##tray_menu.addAction( hide_action )
        
        self.fav_menu = QMenu("Favs")
        
        tray_menu = QMenu()
        tray_menu.addAction( self.toggle_window_action )
        tray_menu.addMenu( self.fav_menu )
        tray_menu.addAction( quit_action )
        self.setContextMenu( tray_menu )
    
    def attachDevice(self, device):
        if self.device != None:
            ## disconnect old object
            self.device.favoritiesChanged.disconnect( self.updateFavMenu )
             
        self.device = device
        self.updateFavMenu()

        ## connect new object
        self.device.favoritiesChanged.connect( self.updateFavMenu )

    
    def setIconNeutral(self, icon):
        self.neutralIcon = icon
    
    def setIconIndicator(self, icon):
        self.indicatorIcon = icon
    
    def setNeutral(self):
        if self.neutralIcon != None:
            self.setIcon( self.neutralIcon )
            self.currIconState = 1
            
    def setIndicator(self):
        if self.indicatorIcon != None:
            self.setIcon( self.indicatorIcon )
            self.currIconState = 2
    
    def displayMessage(self, message):
        self.showMessage("Desk", message, QSystemTrayIcon.NoIcon)
        
    def setInfo(self, message):
        self.setToolTip("Desk: " + message)
    
    def changeIcon(self, state):
        if state == True:
            self.setIndicator()
        else:
            self.setNeutral()
            
    def _refreshIcon(self):
        _LOGGER.warn("refreshing icon state: %s", self.currIconState)
        if self.currIconState == 1:
            self.setNeutral()
        elif self.currIconState == 2:
            self.setIndicator()
        else:
            _LOGGER.warn("unsupported state: %s", self.currIconState)
    
    def _icon_activated(self, reason):
#         print("tray clicked, reason:", reason)
        if reason == 3:
            ## clicked
            self._toggleParent()
    
    def _toggleParent(self):
        parent = self.parent()
        if parent.isHidden():
            parent.show()
        else:
            parent.hide()
        self.updateLabel()
    
    def updateFavMenu(self):
        self.fav_menu.clear()
        if self.device == None:
            return
        positions = self.device.favPositions()
        for i in range( len(positions) ):
            fav = positions[i]
            if fav == None:
                continue
            favAction = QAction( str(fav), self)
            favHandler = functools.partial(self.device.moveToFav, i)
            favAction.triggered.connect( favHandler )
            self.fav_menu.addAction( favAction )
        
    def updateLabel(self):
        parent = self.parent()
        if parent.isHidden():
            self.toggle_window_action.setText("Show")
        else:
            self.toggle_window_action.setText("Hide")
    