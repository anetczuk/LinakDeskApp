#
#
#

import gobject
import dbus

from service import Service, RWCharacteristic
from service import GATT_CHRC_IFACE

import linak_dpg_bt.linak_service as linak_service



class GenericAccessService(Service):
    UUID = linak_service.Service.GENERIC_ACCESS.uuid()

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.UUID, True)
        self.add_characteristic(DeviceNameCharacteristic(bus, 0, self))


class DeviceNameCharacteristic(RWCharacteristic):
    UUID = linak_service.Characteristic.CONTROL.uuid()

    def __init__(self, bus, index, service):
        RWCharacteristic.__init__(
                self, bus, index,
                self.UUID,
                service)
        self.value_lvl = "xxx123"
    