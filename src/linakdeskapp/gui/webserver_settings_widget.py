import logging

from . import uiloader
from .qt import pyqtSignal
from .tray_icon import TrayIconTheme
from ..httpserver import LinakHTTPServer

_LOGGER = logging.getLogger(__name__)

UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )

class WebServerSettingsWidget(QtBaseClass):

    logger = None

    def __init__(self, parentWidget=None):
        super().__init__(parentWidget)
        self.web = None
        self.connector = None
        self.webServerPort = 8000

        self.ui = UiTargetClass()
        self.ui.setupUi(self)

        self.ui.enabledCheck.stateChanged.connect(self.__toggleWebServer)
        self.ui.portSpin.valueChanged.connect(self.__onPortChange)

    def attachConnector(self, connector):
        if self.connector is not None:
            ## disconnect old object
            self.connector.connectionStateChanged.disconnect( self._updateConnectionInfo )

        self.logger.info("desk connector attached to webserver %s", connector)
        self.connector = connector
        if self.web is not None:
            self.web.attachConnector(connector)

    def __toggleWebServer(self, state):
        ## state: 0 -- unchecked
        ## state: 2 -- checked
        enabled = (state != 0)
        self.logger.info("Web server toggled to %s", enabled)
        if enabled:
            self.__startWebServer()
        else:
            self.__stopWebServer()

    def __onPortChange(self, value):
        self.logger.info("Web server port changed to %d", value)
        self.__stopWebServer()
        self.webServerPort = value
        self.__startWebServer()

    def __startWebServer(self):
        self.web = LinakHTTPServer(self.connector)
        self.web.run(self.webServerPort)
        if self.connector is not None:
            self.web.attachConnector(self.connector)

    def __stopWebServer(self):
        self.web.stop()

    def loadSettings(self, settings):
        settings.beginGroup( self.objectName() )

        # Enabled?
        self.webServerEnabled = settings.value("webServerEnabled", False, type=bool)
        self.ui.enabledCheck.setChecked(self.webServerEnabled)

        # Port Number
        self.webServerPort = settings.value("webServerPort", 8000, int)
        self.ui.portSpin.setValue(self.webServerPort)

    def saveSettings(self, settings):
        settings.beginGroup( self.objectName() )
        settings.setValue("webServerPort", self.ui.portSpin.value())
        settings.setValue("webServerEnabled", self.ui.enabledCheck.isChecked())

        settings.endGroup()

WebServerSettingsWidget.logger = _LOGGER.getChild(WebServerSettingsWidget.__name__)
