#
#
#

import gobject
import dbus

from service import Service, RCharacteristic, RNCharacteristic
from service import GATT_CHRC_IFACE

import linak_dpg_bt.linak_service as linak_service



class ReferenceOutputService(Service):
    UUID = linak_service.Service.REFERENCE_OUTPUT.uuid()

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.UUID, True)
        self.add_characteristic(OneCharacteristic(bus, 0, self))
        self.add_characteristic(SevenCharacteristic(bus, 1, self))
        self.add_characteristic(EightCharacteristic(bus, 2, self))
        self.add_characteristic(MaskCharacteristic(bus, 3, self))


class OneCharacteristic(RNCharacteristic):
    UUID = linak_service.Characteristic.HEIGHT_SPEED.uuid()

    def __init__(self, bus, index, service):
        RNCharacteristic.__init__(
                self, bus, index,
                self.UUID,
                service)
        
        
class SevenCharacteristic(RNCharacteristic):
    UUID = linak_service.Characteristic.SEVEN.uuid()

    def __init__(self, bus, index, service):
        RNCharacteristic.__init__(
                self, bus, index,
                self.UUID,
                service)  
        

class EightCharacteristic(RNCharacteristic):
    UUID = linak_service.Characteristic.EIGHT.uuid()

    def __init__(self, bus, index, service):
        RNCharacteristic.__init__(
                self, bus, index,
                self.UUID,
                service)        
        

class MaskCharacteristic(RCharacteristic):
    UUID = linak_service.Characteristic.MASK.uuid()

    def __init__(self, bus, index, service):
        RCharacteristic.__init__(
                self, bus, index,
                self.UUID,
                service)
        self.value_lvl = 1
        
        