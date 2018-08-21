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
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from linakdeskcontrol.gui.device_control_widget import DeviceControlWidget as TestWidget
from .device_object_mock import DeviceObjectMock



app = QApplication(sys.argv)



class DeviceControlWidgetTest(unittest.TestCase):
    
    def setUp(self):
        ## Called before testfunction is executed
        self.widget = TestWidget()

    def tearDown(self):
        ## Called after testfunction was executed
        self.widget = None
    
    def test_disconnected(self):
        upPB = self.widget.ui.upPB
        self.assertFalse( upPB.isEnabled() )
        downPB = self.widget.ui.downPB
        self.assertFalse( downPB.isEnabled() )
       
    def test_upPB(self):
        device = DeviceObjectMock("Device#1", "Owner", 83)
        self.widget.attachDevice( device )
        
        positionStart = device.currentPosition()
        
        upPB = self.widget.ui.upPB
        QTest.mousePress(upPB, Qt.LeftButton)
        self.assertEquals(1, device.upCounter)
        self.assertEquals(0, device.downCounter)
        self.assertEquals(0, device.stopCounter)
        
        QTest.qSleep(1000);
        
        QTest.mouseRelease(upPB, Qt.LeftButton)
        self.assertEquals(1, device.upCounter)
        self.assertEquals(0, device.downCounter)
        self.assertEquals(1, device.stopCounter)
        
        positionEnd = device.currentPosition()
        self.assertGreater(positionEnd, positionStart)
       
    def test_downPB(self):
        device = DeviceObjectMock("Device#1", "Owner", 83)
        self.widget.attachDevice( device )
        
        positionStart = device.currentPosition()
        
        downPB = self.widget.ui.downPB
        QTest.mousePress(downPB, Qt.LeftButton)
        self.assertEquals(0, device.upCounter)
        self.assertEquals(1, device.downCounter)
        self.assertEquals(0, device.stopCounter)
        
        QTest.qSleep(1000);
        
        QTest.mouseRelease(downPB, Qt.LeftButton)
        self.assertEquals(0, device.upCounter)
        self.assertEquals(1, device.downCounter)
        self.assertEquals(1, device.stopCounter)
        
        positionEnd = device.currentPosition()
        self.assertLess(positionEnd, positionStart)


