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

try:
    from bluepy.btle import Scanner
except ImportError as e:
    ### No module named <name>
    print(e)
    exit(1)

from gui.device_connector import DeviceConnector
from bt_device_object import BTDeviceObject



class BTDeviceConnector(DeviceConnector):
    
    def __init__(self):
        super().__init__()
        self.itemIndex = -1
        self.devList = []
    
    def scanDevices(self):
        self.devList = []
        
        if os.getuid() != 0:
            print( "Functionality needs root privileges" )
            return 
        
        print( "Scanning bluetooth devices" )
        
        retList = []
        
        scanner = Scanner()
        devices = scanner.scan(10.0)
        
        for dev in devices:
            self.devList.append( dev.addr )
            devName = "%s (%s)" % (dev.addr, dev.addrType)
            retList.append( devName )
#             print( "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi) )
#             for (adtype, desc, value) in dev.getScanData():
#                 print( "  %s = %s" % (desc, value) )

        print( "Scanning finished" )

        return retList
    
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

    def getConnectedDevice(self):
        if self.isConnected() == False:
            return None
        devItem = self.devList[self.itemIndex]
        return BTDeviceObject( devItem )
    
    def connectTo(self, deviceAddress):
        connectedDevice = BTDeviceObject( deviceAddress )
        self.newConnection.emit(connectedDevice)
    
    