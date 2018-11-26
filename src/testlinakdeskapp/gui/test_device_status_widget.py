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
import unittest

from PyQt5.QtWidgets import QApplication

from linakdeskapp.gui.device_status_widget import DeviceStatusWidget as TestWidget
from .device_connector_mock import DeviceConnectorMock



app = QApplication(sys.argv)



class DeviceStatusWidgetTest(unittest.TestCase):
    def setUp(self):
        # # Called before testfunction is executed
        self.widget = TestWidget()

    def tearDown(self):
        # # Called after testfunction was executed
        self.widget = None

    def test_labels_noDevice(self):
        statusInfo = self.widget.ui.statusLabel.text()
        deviceName = self.widget.ui.deviceLabel.text()
        userType = self.widget.ui.userTypeLabel.text()
        devicePosition = self.widget.ui.positionLabel.text()

        self.assertEqual(statusInfo, "disconnected")
        self.assertEqual(deviceName, "")
        self.assertEqual(userType, "")
        self.assertEqual(devicePosition, "")

    def test_labels_connectedDevice(self):
        device = DeviceConnectorMock("Device#1", "Owner", 83)
        self.widget.attachConnector(device)

        statusInfo = self.widget.ui.statusLabel.text()
        deviceName = self.widget.ui.deviceLabel.text()
        userType = self.widget.ui.userTypeLabel.text()
        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(statusInfo, "connected")
        self.assertEqual(deviceName, "Device#1")
        self.assertEqual(userType, "Owner")
        self.assertEqual(devicePosition, "83 cm")

    def test_labels_positionChange(self):
        device = DeviceConnectorMock("Device#1", "Owner", 83)
        self.widget.attachConnector(device)

        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(devicePosition, "83 cm")

        device.setPosition(77)

        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(devicePosition, "77 cm")

        device.setPosition(99)

        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(devicePosition, "99 cm")

    def test_attach_None(self):
        device = DeviceConnectorMock("Device#1", "Owner", 83)
        self.widget.attachConnector(device)

        statusInfo = self.widget.ui.statusLabel.text()
        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(statusInfo, "connected")
        self.assertEqual(devicePosition, "83 cm")

        self.widget.attachConnector(None)

        device.setPosition(55)

        statusInfo = self.widget.ui.statusLabel.text()
        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(statusInfo, "disconnected")
        self.assertEqual(devicePosition, "")

    def test_attach_twoDevices(self):
        device1 = DeviceConnectorMock("Device#1", "Owner", 83)
        device2 = DeviceConnectorMock("Device#2", "Guest", 93)

        self.widget.attachConnector(device1)
        self.widget.attachConnector(device2)

        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(devicePosition, "93 cm")

        device1.setPosition(55)
        device1.disconnect()

        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(devicePosition, "93 cm")

