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


from linakdeskcontrol.gui.device_object import DeviceObject



class DeviceObjectMock(DeviceObject):
    
    def __init__(self, name, position = None):
        super().__init__()
        
        self.connectionCounter = 0
        self.positionCounter = 0
        self.upCounter = 0
        self.downCounter = 0
        self.stopCounter = 0
        
        self.connectionChanged.connect( self._connectionChanged )
        self.positionChanged.connect( self._positionChanged )
        
        self.connected = True
        self.deviceName = name
        if position != None:
            self.currPosition = position
        else:
            self.currPosition = 90
    
    def isConnected(self):
        return self.connected
    
    def disconnect(self):
        self.connected = False
        self.connectionChanged.emit(self.connected)
    
    def name(self):
        return self.deviceName
    
    def favSlotsNumber(self):
        return 5
    
    def _connectionChanged(self, newConnection):
        self.connectionCounter += 1
        
    def _positionChanged(self):
        self.positionCounter += 1
        
    def moveUp(self):
        self.upCounter += 1
        self.setPosition( self.currPosition + 1 )
        
    def moveDown(self):
        self.downCounter += 1
        self.setPosition( self.currPosition - 1 )
        
    def stopMoving(self):
        self.stopCounter += 1
    
    