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


from . import uiloader



UiTargetClass, QtBaseClass = uiloader.loadUiFromClassName( __file__ )



class DeviceControlWidget(QtBaseClass):
    def __init__(self):
        super().__init__()
        
        self.device = None
        
        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self.ui.upPB.pressed.connect(self._goingUp)
        self.ui.upPB.released.connect(self._stopMoving)
        self.ui.downPB.pressed.connect(self._goingDown)
        self.ui.downPB.released.connect(self._stopMoving)
        
#         # Make some local modifications.
# #         self.ui.colorDepthCombo.addItem("2 colors (1 bit per pixel)")
#          
#         ## Connect up the buttons.
#         self.ui.connectPB.clicked.connect(self._connectToSelected)
#         self.finished.connect(self._setFinished)

    def attachDevice(self, device):
        self.device = device
        
#         if self.device != None:
#             ## disconnect old device
#             self.device.connectionChanged.disconnect( self._refreshWidget )
#             self.device.positionChanged.disconnect( self._refreshPosition )
#             
#         self.device = device
#         if self.device == None:
#             self._refreshWidget(False)
#             return
#         
#         self._refreshWidget(True)
#         
#         ## connect new device
#         self.device.connectionChanged.connect( self._refreshWidget )
#         self.device.positionChanged.connect( self._refreshPosition )

#     def attachConnector(self, connector):
#         self.connector = connector
# 
#     def getFinishedState(self):
#         return self.finishedState
# 
#     def _scanDevices(self):
# #         print "Scanning for devices"
#         self.ui.devicesView.clear()
#         foundItems = self.connector.scanDevices()
# #         print "Found:", foundItems
#         for item in foundItems:
#             self.ui.devicesView.addItem(item)
#         
#     def _connectToSelected(self):
#         currRow = self.ui.devicesView.currentRow()
#         if currRow < 0:
#             return
# #         print "Connecting to device nr", currRow
#         self.connector.connect(currRow)
#         self.accept()
         
    def _goingUp(self):
        self.device.moveUp()
    
    def _goingDown(self):
        self.device.moveDown()
        
    def _stopMoving(self):
        self.device.stopMoving()
        

