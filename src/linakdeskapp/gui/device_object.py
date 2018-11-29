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


import abc
from .qt import QObject, pyqtSignal


QObjectMeta = type(QObject)


class QAbstractMeta(QObjectMeta, abc.ABCMeta):
    """
    Shared meta class of QObject's meta and ABCMeta.

    This is workaround of metaclass conflict:
    TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
    """
    pass


class DeviceObject(QObject, metaclass=QAbstractMeta):

    connectionStateChanged  = pyqtSignal()
    positionChanged         = pyqtSignal()
    speedChanged            = pyqtSignal()
    settingChanged          = pyqtSignal()
    favoritiesChanged       = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    @abc.abstractmethod
    def name(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def deviceType(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def userType(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def capabilities(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def sendDeskHeight(self, cmValue):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def reminder(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def reminderValues(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def reminderSettings(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def readCapabilities(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def readReminderState(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def sendReminderState(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def activateDisplay(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def currentPosition(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def currentSpeed(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def favorities(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def favPositions(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def setFavPosition(self, favIndex, newPosition):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def favSlotsNumber(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def favValues(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def readFavoritiesState(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def sendFavoriteState(self, favIndex):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def sendFavoritiesState(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def moveUp(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def moveDown(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def moveToTop(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def moveToBottom(self):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def moveToFav(self, favIndex):
        raise NotImplementedError('You need to define this method in derived class!')

    @abc.abstractmethod
    def stopMoving(self):
        raise NotImplementedError('You need to define this method in derived class!')

    def positionCm(self):
        currPos = self.currentPosition()
        return str(currPos) + " cm"

