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


from PyQt5 import QtCore

from gui.device_object import DeviceObject

from linak_dpg_bt.linak_device import LinakDesk



class BTDeviceObject(DeviceObject):

    def __init__(self, deviceAddr):
        super().__init__()
        self.desk = LinakDesk( deviceAddr )
        self.desk.read_dpg_data()
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._handleBTNotifications)
        self.timer.start(100)           ## 10 times per second
 
#     def isConnected(self):
#         return True
     
    def name(self):
        ## self.desk.name is of type 'bytes'
        return self.desk.name.decode("utf-8") 
 
    def currentPosition(self):
        return self.desk.read_current_position()
 
    def favSlotsNumber(self):
        return self.desk.read_favorite_number()
     
    def moveUp(self):
        self.desk.moveUp()
         
    def moveDown(self):
        self.desk.moveDown()
         
    def stopMoving(self):
        self.desk.stopMoving()

#     def _setPositionRaw(self, newPosition):
#         raise NotImplementedError('You need to define this method in derived class!')
    
    def _handleBTNotifications(self):
        self.desk.processNotifications()
    
    