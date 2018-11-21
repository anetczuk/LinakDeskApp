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


import unittest

from .device_connector_mock import DeviceConnectorMock



class DeviceConnectorTest(unittest.TestCase):
    def setUp(self):
        ## Called before testfunction is executed
        self.connector = DeviceConnectorMock()
  
    def tearDown(self):
        ## Called after testfunction was executed
        self.connector = None
       
    def test_scanDevices(self):
        devices = self.connector.scanDevices()
        self.assertEqual(devices[0].name, "Desk1")
        self.assertEqual(devices[1].name, "Desk2")
        
    def test_connect(self):
        self.assertFalse( self.connector.isConnected() )
        self.assertEqual( self.connector.address(), None )
        self.assertEqual( self.connector.connectionCounter, 0 )
        
        self.connector.connectTo("aaa")
        
        self.assertTrue( self.connector.isConnected() )
        self.assertEqual( self.connector.address(), "aaa" )
        self.assertEqual( self.connector.connectionCounter, 1 )
        
        self.connector.scanDevices()
        
        self.assertTrue( self.connector.isConnected() )
        self.assertEqual( self.connector.address(), "aaa" )
        self.assertEqual( self.connector.connectionCounter, 1 )
    
    def test_name(self):
        self.connector.connectTo("Device#1")
        
        devName = self.connector.name()
        self.assertEqual( devName, "Custom Desk")
                
    def test_positionCm(self):
        self.connector.connectTo("Device#1")
        
        self.assertEqual( self.connector.positionCounter, 0)
        
        self.connector.setPosition(33)
        position = self.connector.positionCm()
        self.assertEqual( position, "33 cm")
        self.assertEqual( self.connector.positionCounter, 1)

    def test_moveUp(self):
        self.connector.connectTo("Device#1")
        
        self.assertEqual( self.connector.positionCounter, 0)
        self.connector.moveUp()
        self.assertEqual( self.connector.positionCounter, 1)
        
    def test_moveDown(self):
        self.connector.connectTo("Device#1")
        
        self.assertEqual( self.connector.positionCounter, 0)
        self.connector.moveDown()
        self.assertEqual( self.connector.positionCounter, 1)

