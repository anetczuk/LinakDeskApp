#
#
#

import gobject
import dbus

from service import Service, Characteristic, WWCharacteristic
from service import GATT_CHRC_IFACE

import linak_dpg_bt.linak_service as linak_service



class ReferenceInputService(Service):
    UUID = linak_service.Service.REFERENCE_INPUT.uuid()

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.UUID, True)
        self.add_characteristic(Ctrl1Characteristic(bus, 0, self))


class Ctrl1Characteristic(WWCharacteristic):
    UUID = linak_service.Characteristic.CTRL1.uuid()

    def __init__(self, bus, index, service):
        WWCharacteristic.__init__(
                self, bus, index,
                self.UUID,
                service)

        
    