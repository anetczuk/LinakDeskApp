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
from . import tray_icon
from . import resources
from .qt import qApp, QIcon, QtCore

from linakdeskapp.gui.devices_list_dialog import DevicesListDialog
from linakdeskapp.gui.device_connector import ConnectionState


_LOGGER = logging.getLogger(__name__)


UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )


class MainWindow(QtBaseClass):
    def __init__(self):
        super().__init__()
        self.device = None
        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self.settingsFilePath = None
        
        self.statusBar().showMessage("Ready")
        
        self.iconDict             = IconDictionary()
        self.currentTheme         = None
        self.currentPositionState = None
        
        self.trayIcon = tray_icon.TrayIcon(self)
        self.trayIcon.setToolTip("Linak desk")
        
        self.setIconTheme( tray_icon.TrayIconTheme.WHITE )
        
        self.ui.appSettings.showMessage.connect( self.trayIcon.displayMessage )
        self.ui.appSettings.stateInfoChanged.connect( self.trayIcon.setInfo )
        self.ui.appSettings.iconThemeChanged.connect( self.setIconTheme )
        self.ui.appSettings.indicatePositionChange.connect( self._changePositionIcon )
        
        self.trayIcon.show()

    def attachConnector(self, connector, address):
        if self.device is not None:
            ## disconnect old object
            self.device.connectionStateChanged.disconnect( self._updateConnectionInfo )
            
        self.device = connector
        
        self.ui.deviceControl.attachConnector( self.device )
        self.ui.deviceSettings.attachConnector( self.device )
        self.ui.appSettings.attachConnector( self.device )
        self.trayIcon.attachConnector( self.device )
        
        if self.device is not None:
            ## connect new object
            self.device.connectionStateChanged.connect( self._updateConnectionInfo )
        
        if address is not None:
            self.device.connectTo(address)
        else:
            self._tryReconnectOnStartup()

    def _tryReconnectOnStartup(self):
        reconnectAddress = self.ui.appSettings.startupReconnectAddress()
        if reconnectAddress is None:
            return
        _LOGGER.debug("trying reconnect on startup")
        self.device.connectTo( reconnectAddress )

    def setIconTheme(self, theme: tray_icon.TrayIconTheme):
        _LOGGER.debug("setting tray theme: %r", theme)
        
        self.currentTheme = theme
        
        connectedIcon = self.iconDict.getIcon( self.currentTheme.connected )
        self.setWindowIcon( connectedIcon )
        
        self._updateTrayIcon()

    def _changePositionIcon(self, state):
        ## state is True means indicating, otherwise nromal
        self.currentPositionState = state
        self._updateTrayIcon()

    def _updateConnectionInfo(self):
        ## whenever connection status changes then reset position status
        self.currentPositionState = None    
        self._updateTrayIcon()
        
    def _updateTrayIcon(self):
        connection = self.getDeviceConnectionStatus()
        if connection != ConnectionState.CONNECTED:
            currIcon = self.iconDict.getIcon( self.currentTheme.disconnected )
            self.trayIcon.setIcon( currIcon )
            return
        ## connected -- normal or indicating
        if self.currentPositionState is True:
            indicIcon = self.iconDict.getIcon( self.currentTheme.indicating )
            self.trayIcon.setIcon( indicIcon )
        else:
            connectedIcon = self.iconDict.getIcon( self.currentTheme.connected )
            self.trayIcon.setIcon( connectedIcon )

    def getDeviceConnectionStatus(self):
        if self.device is None:
            return ConnectionState.DISCONNECTED
        return self.device.getConnectionStatus()

    def loadSettings(self):
        settings = self.getSettings()
        _LOGGER.debug( "loading app state from %s", settings.fileName() )
        self.ui.appSettings.loadSettings( settings )
        
        ## restore widget state and geometry
        settings.beginGroup( self.objectName() )
        geometry = settings.value("geometry")
        state = settings.value("windowState")
        if geometry is not None:
            self.restoreGeometry( geometry )
        if state is not None:
            self.restoreState( state )
        settings.endGroup()
        
#         ## store geometry of all widgets        
#         widgets = self.findChildren(QWidget)
#         for w in widgets:
#             wKey = getWidgetKey(w)
#             settings.beginGroup( wKey )
#             geometry = settings.value("geometry")
#             if geometry is not None:
#                 w.restoreGeometry( geometry );            
#             settings.endGroup()
    
    def saveSettings(self):
        settings = self.getSettings()
        _LOGGER.debug( "saving app state to %s", settings.fileName() )
        self.ui.appSettings.saveSettings( settings )
        
        ## store widget state and geometry
        settings.beginGroup( self.objectName() )
        settings.setValue("geometry", self.saveGeometry() )
        settings.setValue("windowState", self.saveState() )
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
#         if self.settingsFilePath is None:
# #             scriptDir = os.path.dirname(os.path.realpath(__file__))
# #             self.settingsFilePath = os.path.realpath( scriptDir + "../../../../tmp/settings.ini" )
#             self.settingsFilePath = "settings.ini"
#         settings = QtCore.QSettings(self.settingsFilePath, QtCore.QSettings.IniFormat, self)
    
        ## store in home directory
        orgName = qApp.organizationName()
        appName = qApp.applicationName()
        settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, orgName, appName, self)
        return settings
    
    # ================================================================

    def closeApplication(self):
        ## slot
        ##self.close()
        self.disconnectFromDevice()
        qApp.quit()

    def connectToDevice(self):
        ## slot
        deviceDialog = DevicesListDialog(self)
        deviceDialog.attachConnector(self.device)
        deviceDialog.exec_()                            ### modal mode
    
    def reconnectDevice(self):
        ## slot    
        self.device.reconnect()
    
    def disconnectFromDevice(self):
        ## slot    
        self.device.disconnect()
        
    # ===============================================================

    def closeEvent(self, event):
        # Override closeEvent, to intercept the window closing event
        event.ignore()
        self.hide()
        self.trayIcon.show()
    
    def showEvent(self, event):
        self.trayIcon.updateLabel()
    
    def hideEvent(self, event):
        self.trayIcon.updateLabel()


class IconDictionary():
    
    def __init__(self):
        self.icons = dict()
    
    def getIcon(self, fileName: str):
        if fileName in self.icons:
            return self.icons[fileName]
        iconPath = resources.getImagePath( fileName )
        appIcon = QIcon( iconPath )
        self.icons[fileName] = appIcon
        return appIcon


def getWidgetKey(widget):
    if widget is None:
        return None
    retKey = widget.objectName()
    widget = widget.parent()
    while widget is not None:
        retKey = widget.objectName() + "-" + retKey
        widget = widget.parent()
    return retKey

