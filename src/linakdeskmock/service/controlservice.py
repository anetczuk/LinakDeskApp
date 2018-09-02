#
#
#

import gobject
import dbus

from service import Service, Characteristic, RNCharacteristic, WWCharacteristic
from service import GATT_CHRC_IFACE

import linak_dpg_bt.linak_service as linak_service



class ControlService(Service):
    UUID = linak_service.Service.CONTROL.uuid()

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.UUID, True)
        self.add_characteristic(ErrorCharacteristic(bus, 0, self))
        self.add_characteristic(ControlCharacteristic(bus, 1, self))


class ControlCharacteristic(WWCharacteristic):
    UUID = linak_service.Characteristic.CONTROL.uuid()

    def __init__(self, bus, index, service):
        WWCharacteristic.__init__(
                self, bus, index,
                self.UUID,
                service)

    ### write:
    ## 255, 0  -- STOP_MOVEMENT
    ## 254, 0  -- UNDEFINED
    
    def writeValueHandler(self, value):
        command = int(value[0])

        if command == 70:
            print "MOVE_1_DOWN request received", command, hex(command)
            return
        if command == 71:
            print "MOVE_1_UP request received", command, hex(command)
            return
        if command == 254:
            print "UNDEFINED request received", command, hex(command)
            return
        if command == 255:
            print "STOP_MOVEMENT request received", command, hex(command)
            return

        print "Unknown CONTROL command code:", command, hex(command)
        
        
        
class ErrorCharacteristic(RNCharacteristic):
    UUID = linak_service.Characteristic.ERROR.uuid()

    def __init__(self, bus, index, service):
        RNCharacteristic.__init__(
                self, bus, index,
                self.UUID,
                service)  
        
