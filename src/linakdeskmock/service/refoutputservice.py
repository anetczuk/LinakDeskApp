#
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
        
        