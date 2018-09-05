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


from gui.device_object import DeviceObject

from linak_dpg_bt.linak_device import LinakDesk
from linak_dpg_bt.desk_mover import DeskMoverThread



class BTDeviceObject(DeviceObject):

    def __init__(self, deviceAddr):
        super().__init__()
        self.desk = LinakDesk( deviceAddr )
        ##self.desk.read_dpg_data()
        self.desk.initialize()
        self.desk.set_position_change_callback( self._handleBTPositionChange )
        self.desk.set_speed_change_callback( self._handleBTSpeedChange )
 
        self.mover = DeskMoverThread( self.desk )
        
        
#     def isConnected(self):
#         return True
     
    def name(self):
        return self.desk.name
    
    def userType(self):
        return self.desk.userType
 
    def currentPosition(self):
        return self.desk.read_current_position()
    
    def currentSpeed(self):
        return self.desk.read_current_speed()
 
    def favSlotsNumber(self):
        return self.desk.read_favorite_number()
    
    def favValues(self):
        return self.desk.read_favorite_values()
    
    def moveUp(self):
        self.mover.moveUp()
         
    def moveDown(self):
        self.mover.moveDown()
        
    def moveToFav(self, favIndex):
        self.mover.moveToFav(favIndex)
         
    def stopMoving(self):
        self.mover.stopMoving()

    def _handleBTPositionChange(self):
        self.positionChanged.emit()
        
    def _handleBTSpeedChange(self):
        self.speedChanged.emit()
        