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
    
    def __init__(self, name, userType, position = None):
        super().__init__()
        
        self.positionCounter = 0
        self.upCounter = 0
        self.downCounter = 0
        self.stopCounter = 0
        
        self.positionChanged.connect( self._positionChanged )
        
        self.connected = True
        self.deviceName = name
        self.devType = "DPG Linak"
        self.caps = "a b c"
        self.typeOfUser = userType
        if position != None:
            self.currPosition = position
        else:
            self.currPosition = 90
    
    def name(self):
        return self.deviceName
    
    def deviceType(self):
        return self.devType
    
    def capabilities(self):
        return self.caps

    def userType(self):
        return self.typeOfUser

    def currentPosition(self):
        return self.currPosition
    
    def currentSpeed(self):
        return 0
    
    def favSlotsNumber(self):
        return len( self.favValues() )

    def favValues(self):
        return [11, 22, 33, 44, 55]

    def moveUp(self):
        self.upCounter += 1
        self.setPosition( self.currPosition + 1 )
        
    def moveDown(self):
        self.downCounter += 1
        self.setPosition( self.currPosition - 1 )
        
    def moveToFav(self, favIndex):
        favList = self.favValues()
        fav = favList[favIndex]
        self.setPosition( fav )
        
    def stopMoving(self):
        self.stopCounter += 1
    
    def _setPositionRaw(self, newPosition):
        self.currPosition = newPosition
    
    def _positionChanged(self):
        self.positionCounter += 1
    
    