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


from .qt import QObject, pyqtSignal


class DeviceObject(QObject):

    connectionStateChanged  = pyqtSignal()
    positionChanged         = pyqtSignal()
    speedChanged            = pyqtSignal()
    settingChanged          = pyqtSignal()
    favoritiesChanged       = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def name(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def deviceType(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def userType(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def capabilities(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def sendDeskHeight(self, cmValue):
        raise NotImplementedError('You need to define this method in derived class!')

    def reminder(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def reminderValues(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def reminderSettings(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def readCapabilities(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def readReminderState(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def sendReminderState(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def activateDisplay(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def currentPosition(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def currentSpeed(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def favorities(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def favPositions(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def setFavPosition(self, favIndex, newPosition):
        raise NotImplementedError('You need to define this method in derived class!')

    def favSlotsNumber(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def favValues(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def readFavoritiesState(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def sendFavoriteState(self, favIndex):
        raise NotImplementedError('You need to define this method in derived class!')

    def sendFavoritiesState(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def moveUp(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def moveDown(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def moveToTop(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def moveToBottom(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def moveToFav(self, favIndex):
        raise NotImplementedError('You need to define this method in derived class!')

    def stopMoving(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def _setPositionRaw(self, newPosition):
        raise NotImplementedError('You need to define this method in derived class!')

    def positionCm(self):
        currPos = self.currentPosition()
        return str(currPos) + " cm"

    def setPosition(self, newPosition):
        self._setPositionRaw(newPosition)
        self.positionChanged.emit()

