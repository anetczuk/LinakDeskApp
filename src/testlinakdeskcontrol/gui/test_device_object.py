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

from .device_object_mock import DeviceObjectMock



class DeviceObjectTest(unittest.TestCase):
    def setUp(self):
        ## Called before testfunction is executed
        self.object = DeviceObjectMock("Device#1")
  
    def tearDown(self):
        ## Called after testfunction was executed
        self.object = None
       
    def test_isConnected(self):
        self.assertTrue( self.object.isConnected() )
        self.object.disconnect()        
        self.assertFalse( self.object.isConnected() )
        
    def test_name(self):
        devName = self.object.name()
        self.assertEqual( devName, "Device#1")
                
    def test_positionCm(self):
        self.assertEqual( self.object.connectionCounter, 0)
        self.assertEqual( self.object.positionCounter, 0)
        
        self.object.setPosition(33)
        position = self.object.positionCm()
        self.assertEqual( position, "33 cm")
        self.assertEqual( self.object.positionCounter, 1)
        
        self.object.disconnect()        
        self.assertFalse( self.object.isConnected() )
        self.assertEqual( self.object.connectionCounter, 1)

