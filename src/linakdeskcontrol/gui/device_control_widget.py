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
    
    def __init__(self, parentWidget = None):
        super().__init__(parentWidget)
        
        self.device = None
        
        self.ui = UiTargetClass()
        self.ui.setupUi(self)
        
        self.ui.upPB.setEnabled(False)
        self.ui.downPB.setEnabled(False)
        
        self.ui.upPB.pressed.connect(self._goingUp)
        self.ui.upPB.released.connect(self._stopMoving)
        self.ui.downPB.pressed.connect(self._goingDown)
        self.ui.downPB.released.connect(self._stopMoving)

    def attachDevice(self, device):
        self.ui.deviceStatus.attachDevice(device)
        self.device = device
        if self.device == None:
            self.ui.upPB.setEnabled(False)
            self.ui.downPB.setEnabled(False)
            return
        self.ui.upPB.setEnabled(True)
        self.ui.downPB.setEnabled(True)

    def _goingUp(self):
        if self.device == None:
            return
        self.device.moveUp()
    
    def _goingDown(self):
        if self.device == None:
            return
        self.device.moveDown()
        
    def _stopMoving(self):
        if self.device == None:
            return
        self.device.stopMoving()
        
