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


import os
import logging

try:
    from bluepy.btle import Scanner
except ImportError as e:
    ### No module named <name>
    print(e)
    exit(1)

from .gui.qt import QtCore

from .gui.device_object import DeviceObject
from .gui.device_connector import DeviceConnector, ScanItem, ConnectionState

from linak_dpg_bt.linak_device import LinakDesk
from linak_dpg_bt.desk_mover import DeskMoverThread


_LOGGER = logging.getLogger(__name__)


class BTDeviceConnector(DeviceConnector, DeviceObject):

    def __init__(self):
        DeviceConnector.__init__(self)
        DeviceObject.__init__(self)

        self.connectionStatus = ConnectionState.DISCONNECTED
        self.devList = []

        self.desk = None
        self.mover = None
        self.recentAddress = None

        self.threadpool = QtCore.QThreadPool()

    def scanDevices(self):
        self.devList = []

        if os.getuid() != 0:
            _LOGGER.debug( "Functionality needs root privileges" )
            return

        _LOGGER.debug( "Scanning bluetooth devices" )

        retList = []

        scanner = Scanner()
        devices = scanner.scan(10.0)

        for dev in devices:
            self.devList.append( dev.addr )
            devName = "%s (%s)" % (dev.addr, dev.getValueText(9))
            item = ScanItem( devName, dev.addr )
            retList.append( item )
#             print( "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi) )
#             for (adtype, desc, value) in dev.getScanData():
#                 print( "  %s = %s" % (desc, value) )

        _LOGGER.debug( "Scanning finished" )

        return retList

    ## ==================================================================

    def address(self):
        return self.recentAddress

    def getConnectionStatus(self) -> ConnectionState:
        return self.connectionStatus

    def connectTo(self, deviceAddr):
        if self.connectionStatus == ConnectionState.CONN_IN_PROGRESS:
            _LOGGER.debug("unable to connect -- connection in progress")
            return
        self.disconnect()
        self.recentAddress = deviceAddr
        if deviceAddr is None:
            return
        self._changeConnectionStatus(ConnectionState.CONN_IN_PROGRESS)
        worker = ThreadWorker( self._initializeDevice )
        self.threadpool.start(worker)

    def _initializeDevice(self):
        device = LinakDesk( self.recentAddress )
        ##self.desk.read_dpg_data()
        connected = device.initialize()
        if connected is False:
            self.desk = None
            self._changeConnectionStatus(ConnectionState.DISCONNECTED)
            return

        device.set_position_change_callback( self._handleBTPositionChange )
        device.set_speed_change_callback( self._handleBTSpeedChange )
        device.add_setting_callback( self._handleBTSettingChange )
        device.add_favorities_callback( self._handleBTFavoritiesChange )
        device.set_disconnected_callback( self._handleBTDisconnection )

        self.desk = device
        self.mover = DeskMoverThread( self.desk )
        self._changeConnectionStatus(ConnectionState.CONNECTED)

    def reconnect(self):
        self.connectTo( self.recentAddress )

    def disconnect(self):
        if self.connectionStatus == ConnectionState.CONN_IN_PROGRESS:
            _LOGGER.debug("unable to disconnect -- connection in progress")
            return
        if self.desk is None:
            self._changeConnectionStatus(ConnectionState.DISCONNECTED)
            return
        self.desk.disconnect()
        self._changeConnectionStatus(ConnectionState.DISCONNECTED)

    def _changeConnectionStatus(self, newStatus):
        if self.connectionStatus == newStatus:
            return
        _LOGGER.debug("changing connection state to %s", newStatus)
        self.connectionStatus = newStatus
        self.connectionStateChanged.emit()

    ### =================================================================

    def name(self):
        return self.desk.name

    def deviceType(self):
        return self.desk.deviceType

    def userType(self):
        return self.desk.userType

    def capabilities(self):
        return self.desk.capabilities

    def sendDeskHeight(self, cmValue):
        self.desk.send_desk_height(cmValue)

    def reminder(self):
        return self.desk.reminder

    def reminderValues(self):
        return self.desk.read_reminder_values()

    def reminderSettings(self):
        return self.desk.reminder_settings()

    def readCapabilities(self):
        return self.desk.read_capabilities()

    def readReminderState(self):
        return self.desk.read_reminder_state()

    def sendReminderState(self):
        return self.desk.send_reminder_state()

    def activateDisplay(self):
        return self.desk.activate_display()

    def currentPosition(self):
        return self.desk.read_current_position()

    def currentSpeed(self):
        return self.desk.read_current_speed()

    def favorities(self):
        return self.desk.favorities()

    def favPositions(self):
        return self.desk.read_favorite_positions()

    def setFavPosition(self, favIndex, newPosition):
        self.desk.set_favorite_position(favIndex, newPosition)

    def favSlotsNumber(self):
        return self.desk.read_favorite_number()

    ## with 'cm' suffix
    def favValues(self):
        return self.desk.read_favorite_values()

    def readFavoritiesState(self):
        return self.desk.read_favorities_state()

    def sendFavoriteState(self, favIndex):
        return self.desk.send_fav(favIndex)

    def sendFavoritiesState(self):
        return self.desk.send_favorities_state()

    def moveUp(self):
        self.mover.moveUp()

    def moveDown(self):
        self.mover.moveDown()

    def moveToTop(self):
        self.mover.moveToTop()

    def moveToBottom(self):
        self.mover.moveToBottom()

    def moveToFav(self, favIndex):
        self.mover.moveToFav(favIndex)

    def stopMoving(self):
        self.mover.stopMoving()

    ## =====================================================

    def _handleBTPositionChange(self):
        self.positionChanged.emit()

    def _handleBTSpeedChange(self):
        self.speedChanged.emit()

    def _handleBTSettingChange(self):
        self.settingChanged.emit()

    def _handleBTFavoritiesChange(self, favNumber):
        self.favoritiesChanged.emit(favNumber - 1)

    def _handleBTDisconnection(self):
        self._changeConnectionStatus(ConnectionState.DISCONNECTED)

    @staticmethod
    def printDescription(deviceAddr):
        if deviceAddr is None:
            return False
        desk = LinakDesk( deviceAddr )
        desk.print_services()
        return True


class ThreadWorker(QtCore.QRunnable):
    """Worker thread."""

    def __init__(self, function):
        super().__init__()
        self.setAutoDelete(True)
        self.call = function

    def run(self):
        """Your code goes in this function."""
        _LOGGER.debug("Worker start")
        self.call()
        _LOGGER.debug("Worker complete")

