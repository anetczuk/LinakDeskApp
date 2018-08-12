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

from linakdeskcontrol.gui.device_status_widget import DeviceStatusWidget as TestWidget
from .device_object_mock import DeviceObjectMock



app = QApplication(sys.argv)



class DeviceStatusWidgetTest(unittest.TestCase):
    def setUp(self):
        ## Called before testfunction is executed
        self.widget = TestWidget()

    def tearDown(self):
        ## Called after testfunction was executed
        self.widget = None
       
    def test_labels_noDevice(self):
        statusInfo = self.widget.ui.statusLabel.text()
        deviceName = self.widget.ui.nameLabel.text()
        devicePosition = self.widget.ui.positionLabel.text()
        favsNumber = self.widget.ui.favsNumLabel.text()
        
        self.assertEqual(statusInfo, "disconnected")
        self.assertEqual(deviceName, "")
        self.assertEqual(devicePosition, "")
        self.assertEqual(favsNumber, "")
        
    def test_labels_connectedDevice(self):
        device = DeviceObjectMock("Device#1", 83)
        self.widget.attachDevice( device )
        
        statusInfo = self.widget.ui.statusLabel.text()
        deviceName = self.widget.ui.nameLabel.text()
        devicePosition = self.widget.ui.positionLabel.text()
        favsNumber = self.widget.ui.favsNumLabel.text()
        self.assertEqual(statusInfo, "connected")
        self.assertEqual(deviceName, "Device#1")
        self.assertEqual(devicePosition, "83 cm")
        self.assertEqual(favsNumber, "5")
    
    def test_labels_positionChange(self):
        device = DeviceObjectMock("Device#1", 83)
        self.widget.attachDevice( device )
        
        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(devicePosition, "83 cm")
        
        device.setPosition(77)
        
        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(devicePosition, "77 cm")
        
        device.setPosition(99)
        
        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(devicePosition, "99 cm")
        
    def test_labels_disconnect(self):
        device = DeviceObjectMock("Device#1", 83)
        self.widget.attachDevice( device )
        
        statusInfo = self.widget.ui.statusLabel.text()
        deviceName = self.widget.ui.nameLabel.text()
        devicePosition = self.widget.ui.positionLabel.text()
        favsNumber = self.widget.ui.favsNumLabel.text()
        self.assertEqual(statusInfo, "connected")
        self.assertEqual(deviceName, "Device#1")
        self.assertEqual(devicePosition, "83 cm")
        self.assertEqual(favsNumber, "5")
                
        device.disconnect()
        
        statusInfo = self.widget.ui.statusLabel.text()
        deviceName = self.widget.ui.nameLabel.text()
        devicePosition = self.widget.ui.positionLabel.text()
        favsNumber = self.widget.ui.favsNumLabel.text()
        self.assertEqual(statusInfo, "disconnected")
        self.assertEqual(deviceName, "")
        self.assertEqual(devicePosition, "")
        self.assertEqual(favsNumber, "")
        
    def test_attach_None(self):
        device = DeviceObjectMock("Device#1", 83)
        self.widget.attachDevice( device )

        statusInfo = self.widget.ui.statusLabel.text()
        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(statusInfo, "connected")
        self.assertEqual(devicePosition, "83 cm")
        
        self.widget.attachDevice( None )
        
        device.setPosition(55)
        
        statusInfo = self.widget.ui.statusLabel.text()
        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(statusInfo, "disconnected")
        self.assertEqual(devicePosition, "")
        
    def test_attach_twoDevices(self):
        device1 = DeviceObjectMock("Device#1", 83)
        device2 = DeviceObjectMock("Device#2", 93)
         
        self.widget.attachDevice( device1 )
        self.widget.attachDevice( device2 )
         
        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(devicePosition, "93 cm")
         
        device1.setPosition(55)
        device1.disconnect()
         
        devicePosition = self.widget.ui.positionLabel.text()
        self.assertEqual(devicePosition, "93 cm")

