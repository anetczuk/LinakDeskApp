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
from PyQt5.QtWidgets import QDialog as QDialog
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt

from linakdeskcontrol.gui.devices_list_dialog import DevicesListDialog as TestWidget
from ..device_connector_mock import DeviceConnectorMock



app = QApplication(sys.argv)



class DevicesListDialogTest(unittest.TestCase):
    def setUp(self):
        ## Called before testfunction is executed
        self.widget = TestWidget()
        self.connector = DeviceConnectorMock()
        self.widget.attachConnector( self.connector )

    def tearDown(self):
        ## Called after testfunction was executed
        self.connector = None
        self.widget = None
       
    def test_scan(self):
        pButton = self.widget.ui.scanBTPB
        QTest.mouseClick(pButton, Qt.LeftButton)
        self.assertEqual(2, self.widget.ui.devicesView.count())
        
    def test_connect(self):
        self.widget.ui.devicesView.addItem("Device1")
        self.widget.ui.devicesView.addItem("Device2")
        self.widget.ui.devicesView.setCurrentRow(1)

        self.assertFalse( self.connector.isConnected() )
        self.assertEqual( self.connector.getItemIndex(), -1 )
        self.assertEqual( 0, self.widget.getFinishedState() )

        pButton = self.widget.ui.connectPB
        QTest.mouseClick(pButton, Qt.LeftButton)
        
        self.assertTrue( self.connector.isConnected() )
        self.assertEqual( self.connector.getItemIndex(), 1 )
        self.assertEqual( QDialog.Accepted, self.widget.getFinishedState() )
        
        

