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


from linakdeskapp.gui.device_object import DeviceObject
from linakdeskapp.gui.device_connector import DeviceConnector



def to_bin_string7(data):
    return " ".join( '{:07b}'.format(x) for x in data )



class DeviceMock():
    
    def __init__(self, name, userType, position = None):
        self.connected = True
        self.deviceName = name
        self.devType = "DPG Linak"
        self.caps = "a b c"
        self.typeOfUser = userType
        self.reminderData = "50 10"
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

    def reminder(self):
        return self.reminderData
    
    def reminderValues(self):
        return [(11, 33), (77, 99)]
    
    def reminderSettings(self):
        return ReminderSettingMock()
    
    def readCapabilities(self):
        ## do nothing
        pass
    
    def readReminderState(self):
        ## do nothing
        pass
        
    def sendReminderState(self):
        ## do nothing
        pass

    def activateDisplay(self):
        ## do nothing
        pass
    
    def currentPosition(self):
        return self.currPosition
    
    def currentSpeed(self):
        return 0
    
    def favSlotsNumber(self):
        return len( self.favValues() )

    def favValues(self):
        return [11, 22, 33, 44, 55]

    def favPositions(self):
        return []
    
    def favorities(self):
        return []
    


class DeviceConnectorMock(DeviceConnector, DeviceObject):
    
    def __init__(self, name = None, userType = None, position = None):
        DeviceConnector.__init__(self)
        DeviceObject.__init__(self)
        
        self.itemIndex = -1
        self.devList = ["Desk1", "Desk2"]
        
        self.device = None
        self.recentAddress = None
        if name != None:
            self.device = DeviceMock(name, userType, position)
        
        self.connectionCounter = 0
        self.positionCounter = 0
        self.upCounter = 0
        self.downCounter = 0
        self.stopCounter = 0
        
        self.newConnection.connect( self._connectionArrived )        
        self.positionChanged.connect( self._positionChanged )

    
    def scanDevices(self):
        self.itemIndex = -1
        return self.devList


    # ==============================================================
    
    def address(self):
        return self.recentAddress
    
    def isConnected(self):
        return (self.device != None)
    
    def getItemIndex(self):
        return self.itemIndex
    
    def connectTo(self, deviceAddress):
        self.recentAddress = deviceAddress
        if deviceAddress == None:
            return False
        name = "Desk"
        if self.itemIndex > -1:
            name = self.devList[self.itemIndex]
        self.device = DeviceMock( name, "Owner" )
        self.newConnection.emit()
    
    def connectByIndex(self, itemIndex):
        self.itemIndex = itemIndex
        return self.connectTo("11:22:33:44")
    
    def _connectionArrived(self):
        self.connectionCounter += 1
        
    def _positionChanged(self):
        self.positionCounter += 1
        
    def disconnect(self):
        self.device = None
    
    
    ### ===========================================================
    
    
    def name(self):
        return self.device.name()
    
    def deviceType(self):
        return self.device.deviceType()
    
    def capabilities(self):
        return self.device.capabilities()

    def userType(self):
        return self.device.userType()

    def reminder(self):
        return self.device.reminder()
    
    def reminderValues(self):
        return self.device.reminderValues()
    
    def reminderSettings(self):
        return self.device.reminderSettings()
    
    def readCapabilities(self):
        return self.device.readCapabilities()
    
    def readReminderState(self):
        return self.device.readReminderState()
        
    def sendReminderState(self):
        return self.device.sendReminderState()

    def activateDisplay(self):
        return self.device.activateDisplay()
    
    def currentPosition(self):
        return self.device.currentPosition()
    
    def currentSpeed(self):
        return self.device.currentSpeed()
    
    def favSlotsNumber(self):
        return self.device.favSlotsNumber()

    def favValues(self):
        return self.device.favValues()
    
    def favPositions(self):
        return self.device.favPositions()
    
    def favorities(self):
        return self.device.favorities()


    def moveUp(self):
        self.upCounter += 1
        self.setPosition( self.device.currPosition + 1 )
        
    def moveDown(self):
        self.downCounter += 1
        self.setPosition( self.device.currPosition - 1 )
        
    def moveToTop(self):
        self.upCounter += 10
        self.setPosition( self.device.currPosition + 10 )
    
    def moveToBottom(self):
        self.downCounter += 10
        self.setPosition( self.device.currPosition - 10 )
        
    def moveToFav(self, favIndex):
        favList = self.favValues()
        fav = favList[favIndex]
        self.setPosition( fav )
        
    def stopMoving(self):
        self.stopCounter += 1
    
    def _setPositionRaw(self, newPosition):
        self.device.currPosition = newPosition
    
    
class ReminderSettingMock():
    
    def __init__(self):
        self.cmEnabled   = False
        self.impulseUp   = False
        self.impulseDown = False
        self.wake        = False
        self.lightGuide  = False
    
    def getCmUnit(self):
        return self.cmEnabled
    
    def setCmUnit(self, useCm):
        if useCm == True:
            self.cmEnabled = True
        else:
            self.cmEnabled = False
            
    def getAutomaticUp(self):
        return self.impulseUp
    
    def setAutomaticUp(self, state):
        if state == True:
            self.impulseUp = True
        else:
            self.impulseUp = False
            
    def getAutomaticDown(self):
        return self.impulseDown
    
    def setAutomaticDown(self, state):
        if state == True:
            self.impulseDown = True
        else:
            self.impulseDown = False
                
    def getWake(self):
        return self.wake
        
    def setWake(self, state):
        if state == True:
            self.wake = True
        else: 
            self.wake = False
            
    def getLights(self):
        return self.lightGuide
        
    def setLights(self, state):
        if state == True:
            self.lightGuide = True
        else: 
            self.lightGuide = False
    
    def currentReminderInfo(self):
        return "111/222"
    
    def counter(self):
        return 12345
    
    def state(self):
        flags = 0b00110100
        return to_bin_string7( [flags] )
    
    def getRemindersList(self):
        retList = [] 
        return retList
    
    def getReminderIndex(self):
        return 0

