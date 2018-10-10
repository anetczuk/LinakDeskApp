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


import sys
import os
import logging

from . import uiloader
from . import tray_icon
from .qt import qApp, QApplication, QIcon, QtCore

from linakdeskapp.gui.devices_list_dialog import DevicesListDialog



_LOGGER = logging.getLogger(__name__)


UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )



class MainWindow(QtBaseClass):
    def __init__(self):
        super().__init__()
        self.connector = None
        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self.settingsFilePath = None
        
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        appIcon = QIcon( scriptDir + os.path.sep + 'office-chair.png' )
        self.setWindowIcon( appIcon )
        
        self.statusBar().showMessage("Ready")
        
        ## Init QSystemTrayIcon
        self.trayIcon = tray_icon.TrayIcon(self)
        systemIcon = QIcon( scriptDir + os.path.sep + 'office-chair_gray.png' )
        self.trayIcon.setIcon( systemIcon )
        self.trayIcon.show()
        
        self.ui.appSettings.attachTray( self.trayIcon )

    def attachConnector(self, connector):
        if self.connector != None:
            ## disconnect slot from old object
            self.connector.newConnection.disconnect( self.newConnection )
            
        self.connector = connector
        ## connect slot to new object
        self.connector.newConnection.connect( self.newConnection )

    def _setDevice(self, device):
        self.ui.deviceControl.attachDevice( device )
        self.ui.deviceSettings.attachDevice( device )
        self.ui.appSettings.attachDevice( device )

    def loadSettings(self):
        settings = self.getSettings()
        _LOGGER.debug( "loading app state from %s", settings.fileName() )
        self.ui.appSettings.loadSettings( settings )
        
        ## restore widget state and geometry
        settings.beginGroup( self.objectName() )
        geometry = settings.value("geometry")
        state = settings.value("windowState")
        if geometry != None:
            self.restoreGeometry( geometry );
        if state != None:
            self.restoreState( state );
        settings.endGroup()
    
    def saveSettings(self):
        settings = self.getSettings()
        _LOGGER.debug( "saving app state to %s", settings.fileName() )
        self.ui.appSettings.saveSettings( settings )
        
        ## store widget state and geometry
        settings.beginGroup( self.objectName() )
        settings.setValue("geometry", self.saveGeometry() );
        settings.setValue("windowState", self.saveState() );
        settings.endGroup()
        
        ## force save to file
        settings.sync()        

    def getSettings(self):
#         ## store in app directory
#         if self.settingsFilePath == None:
# #             scriptDir = os.path.dirname(os.path.realpath(__file__))
# #             self.settingsFilePath = os.path.realpath( scriptDir + "../../../../tmp/settings.ini" )
#             self.settingsFilePath = "settings.ini"
#         settings = QtCore.QSettings(self.settingsFilePath, QtCore.QSettings.IniFormat, self)
    
        ## store in home directory
        settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "arnet", "LinakDeskApp", self)
        return settings
        

    # ================================================================


    ## slot
    def newConnection(self, deviceObject):
        if deviceObject == None:
            return
        self._setDevice( deviceObject )
        
    ## slot
    def closeApplication(self):
        ##self.close()
        qApp.quit()

    ## slot
    def connectToDevice(self):
        deviceDialog = DevicesListDialog(self)
        deviceDialog.attachConnector(self.connector)
        deviceDialog.exec_()                            ### modal mode
    
    ## slot    
    def disconnectFromDevice(self):
        self._setDevice( None )

        
    # =======================================


    # Override closeEvent, to intercept the window closing event
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.trayIcon.show()



def execApp():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    sys.exit(app.exec_())

