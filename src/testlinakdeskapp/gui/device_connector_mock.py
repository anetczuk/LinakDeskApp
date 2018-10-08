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


from linakdeskapp.gui.device_connector import DeviceConnector

from .device_object_mock import DeviceObjectMock



class DeviceConnectorMock(DeviceConnector):
    
    def __init__(self):
        super().__init__()
        self.itemIndex = -1
        self.devList = ["Desk1", "Desk2"]
        
        self.connectionCounter = 0
        self.newConnection.connect( self._connectionArrived )
    
    def scanDevices(self):
        self.itemIndex = -1
        return self.devList
    
    def connect(self, itemIndex):
        self.itemIndex = itemIndex
        deviceObject = self.getConnectedDevice()
        if deviceObject != None:
            self.newConnection.emit(deviceObject)


    # ==============================================================
    

    def isConnected(self):
        if self.itemIndex < 0:
            return False
        if self.itemIndex >= len(self.devList):
            return False
        return True
    
    def getItemIndex(self):
        return self.itemIndex

    def getConnectedDevice(self):
        if self.isConnected() == False:
            return None
        devName = self.devList[self.itemIndex]
        return DeviceObjectMock( devName, "Owner" )
    
    def connectTo(self, deviceAddress):
        self.connect(0)
    
    def _connectionArrived(self, deviceObject):
        self.connectionCounter += 1
    