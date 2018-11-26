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


from service import Service, RNCharacteristic, WWCharacteristic

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

