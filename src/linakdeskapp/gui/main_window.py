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
import logging

from . import uiloader
from . import tray_icon
from . import resources
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
        
        self.statusBar().showMessage("Ready")
        
        self.trayIcon = tray_icon.TrayIcon(self)
        self.trayIcon.setToolTip("Linak desk")
        
        self.setIconTheme( tray_icon.TrayIconTheme.WHITE )
        
        self.ui.appSettings.showMessage.connect( self.trayIcon.displayMessage )
        self.ui.appSettings.stateInfoChanged.connect( self.trayIcon.setInfo )
        self.ui.appSettings.indicatePositionChange.connect( self.trayIcon.changeIcon )
        self.ui.appSettings.iconThemeChanged.connect( self.setIconTheme )
        
        self.trayIcon.show()

    def attachConnector(self, connector):
        if self.connector != None:
            ## disconnect slot from old object
            self.connector.newConnection.disconnect( self.newConnection )
            
        self.connector = connector
        ## connect slot to new object
        self.connector.newConnection.connect( self.newConnection )

    def setIconTheme(self, theme: tray_icon.TrayIconTheme):
        _LOGGER.debug("setting tray theme: %r", theme)
        
        fileName = theme.value[0]
        iconPath = resources.getImagePath( fileName )
        appIcon = QIcon( iconPath )
        self.setWindowIcon( appIcon )
        self.trayIcon.setIconNeutral( appIcon )

        fileName = theme.value[1]
        iconPath = resources.getImagePath( fileName )
        appIcon = QIcon( iconPath )
        self.trayIcon.setIconIndicator( appIcon )
        

#         neutralPath = resources.getImagePath('office-chair-gray.png')
#         indicatorPath = resources.getImagePath('office-chair-red-gray.png')
#         self.setIconNeutral( QIcon( neutralPath ) )
#         self.setIconIndicator( QIcon( indicatorPath ) )
#         self.setNeutral()

    def _setDevice(self, device):
        self.ui.deviceControl.attachDevice( device )
        self.ui.deviceSettings.attachDevice( device )
        self.ui.appSettings.attachDevice( device )
        self.trayIcon.attachDevice( device )

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
        
#         ## store geometry of all widgets        
#         widgets = self.findChildren(QWidget)
#         for w in widgets:
#             wKey = getWidgetKey(w)
#             settings.beginGroup( wKey )
#             geometry = settings.value("geometry")
#             if geometry != None:
#                 w.restoreGeometry( geometry );            
#             settings.endGroup()
    
    def saveSettings(self):
        settings = self.getSettings()
        _LOGGER.debug( "saving app state to %s", settings.fileName() )
        self.ui.appSettings.saveSettings( settings )
        
        ## store widget state and geometry
        settings.beginGroup( self.objectName() )
        settings.setValue("geometry", self.saveGeometry() );
        settings.setValue("windowState", self.saveState() );
        settings.endGroup()

#         ## store geometry of all widgets        
#         widgets = self.findChildren(QWidget)
#         for w in widgets:
#             wKey = getWidgetKey(w)
#             settings.beginGroup( wKey )
#             settings.setValue("geometry", w.saveGeometry() );
#             settings.endGroup()
        
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
        self.connector.disconnect()
        qApp.quit()

    ## slot
    def connectToDevice(self):
        deviceDialog = DevicesListDialog(self)
        deviceDialog.attachConnector(self.connector)
        deviceDialog.exec_()                            ### modal mode
    
    ## slot    
    def disconnectFromDevice(self):
        self.connector.disconnect()
        self._setDevice( None )
        
    ## slot    
    def reconnectDevice(self):
        self.connector.reconnect()

        
    # =======================================


    # Override closeEvent, to intercept the window closing event
    def closeEvent(self, event):
        event.ignore()
        self.hide()
        self.trayIcon.show()
    
    def showEvent(self, event):
        self.trayIcon.updateLabel()
    
    def hideEvent(self, event):
        self.trayIcon.updateLabel()
    

def getWidgetKey(widget):
    if widget == None:
        return None
    retKey = widget.objectName()
    widget = widget.parent()
    while widget != None:
        retKey = widget.objectName() + "-"+ retKey
        widget = widget.parent()
    return retKey

def execApp():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    window.show()
    sys.exit(app.exec_())

