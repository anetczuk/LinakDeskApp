#     ClevoKeyboardControl. Control of keyboard backlights.
#
#     Copyright (C) 2018  Arkadiusz Netczuk <dev.arnet@gmail.com>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#


import logging

import datetime
from .qt import QtCore
from .qt import qApp
from .qt import pyqtSignal


_LOGGER = logging.getLogger(__name__)


class QSuspendTimer( QtCore.QObject ):

    logger = None

    resumed = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.lastTime = None
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect( self.checkResumed )

    def start(self):
        self.logger.debug("starting suspension detector")
        self.lastTime = None
        self.timer.start( 1000 )                            ## triggered every second

    def stop(self):
        self.logger.debug("stopping suspension detector")
        self.timer.stop()

    def checkResumed(self):
        if self.lastTime is None:
            self.lastTime = datetime.datetime.now()
            return False
        currTime = datetime.datetime.now()
        timeDiff = currTime - self.lastTime
        secDiff = timeDiff.total_seconds()
        self.lastTime = currTime
        if secDiff < 3.5:
            return False
        self.logger.debug("resumed from suspend / hibernation after %s[s]", secDiff)
        self.resumed.emit()
        return True


QSuspendTimer.logger = _LOGGER.getChild(QSuspendTimer.__name__)


class SingletonMeta(type):
    _instances = {}

    def __call__(self, *args, **kwargs):
        if self not in self._instances:
            self._instances[self] = super(SingletonMeta, self).__call__(*args, **kwargs)
        return self._instances[self]


QObjectMeta = type(QtCore.QObject)


class QSingletonMeta(QObjectMeta, SingletonMeta):
    """
    Shared meta class of QObject's meta and Singleton.

    This is workaround of metaclass conflict:
    TypeError: metaclass conflict: the metaclass of a derived class must be a (non-strict) subclass of the metaclasses of all its bases
    """

    pass


class QSuspendSingleton( QtCore.QObject, metaclass=QSingletonMeta ):
    """Singleton."""

    resumed   = pyqtSignal()
    _instance = None

    def __init__(self):
        super().__init__( qApp )
        self.timer = QSuspendTimer( self )
        self.timer.resumed.connect( self.resumed )
        self.timer.start()

    @classmethod
    def checkResumed(cls):
        timer = QSuspendSingleton().timer
        return timer.checkResumed()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = QSuspendSingleton()
        return cls._instance


class QSuspendDetector( QtCore.QObject ):

    logger = None

    resumed  = pyqtSignal()

    def __init__(self, parent):
        super().__init__( parent )
        self.detector = QSuspendSingleton()

    def start(self):
        self.logger.debug("starting suspension detector")
        self.detector.resumed.connect( self.resumed )

    def stop(self):
        self.logger.debug("stopping suspension detector")
        self.detector.resumed.disconnect( self.resumed )


QSuspendDetector.logger = _LOGGER.getChild(QSuspendDetector.__name__)

