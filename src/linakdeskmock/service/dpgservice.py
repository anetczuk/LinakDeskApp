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


from service import Service, RWWNCharacteristic

import linak_dpg_bt.linak_service as linak_service


class DpgService(Service):
    UUID = linak_service.Service.DPG.uuid()

    def __init__(self, bus, index):
        Service.__init__(self, bus, index, self.UUID, True)
        self.add_characteristic(DpgCharacteristic(bus, 0, self))


class DpgCharacteristic(RWWNCharacteristic):
    UUID = linak_service.Characteristic.DPG.uuid()

    def __init__(self, bus, index, service):
        RWWNCharacteristic.__init__(
                self, bus, index,
                self.UUID,
                service)

    def writeValueHandler(self, value):
        command = value[1]
        if command == 10:
            ## USER_ID command
            print( "GET_SETUP request received", command, hex(command), self.notifying )
            newVal = [0x0B, 0x0]
            self.notifyValue(newVal)
            return
        if command == 128:      ##0x80
            print( "GET_CAPABILITIES request received", command, hex(command), self.notifying )
            newVal = [0x01, 0x02, 0xfc, 0x01]
            self.notifyValue(newVal)
            return
        if command == 129:      ## 0x81
            print( "DESK_OFFSET request received", command, hex(command), self.notifying )
            newVal = [0x01, 0x03, 0x01, 0x62, 0x1b]
            self.notifyValue(newVal)
            return
        if command == 134:      ## 0x86
            ## USER_ID command
            if value[2] == 0:
                print( "USER_ID request received", command, hex(command), self.notifying )
                ## guest
                newVal = [0x01, 0x11, 0x00, 0xA2, 0x68, 0x62, 0x96, 0x4f, 0xfb, 0x9d, 0x45, 0x36, 0xd0, 0xff, 0xbf, 0x6a, 0xfc]
                self.notifyValue(newVal)
            else:
                lockState = value[3]
                print( "USER_ID storage received, lock:", lockState )
                newVal = [0x01, 0x00]
                self.notifyValue(newVal)
            return
        if command == 136:      ## 0x88
            if value[2] == 0:
                print( "REMINDER_SETTING request received", command, hex(command), self.notifying )
                newVal = [0x01, 0x0b, 0x20, 0x37, 0x0a, 0x2d, 0x0f, 0x86, 0x88, 0x00, 0x00]
                self.notifyValue(newVal)
            else:
                print( "REMINDER_SETTING storage received", command, hex(command), self.notifying )
                newVal = [0x01, 0x00]
                self.notifyValue(newVal)
            return
        if command == 137:      ## 0x89
            print( "GET_SET_MEMORY_POSITION_1 request received", command, hex(command), self.notifying )
            newVal = [0x01, 0x07, 0x01, 0xe1, 0x07, 0x8f, 0x87, 0x00, 0x00]
            self.notifyValue(newVal)
            return
        if command == 138:      ## 0x8a
            print( "GET_SET_MEMORY_POSITION_2 request received", command, hex(command), self.notifying )
            newVal = [0x01, 0x07, 0x01, 0xe1, 0x07, 0x8f, 0x87, 0x00, 0x00]
            self.notifyValue(newVal)
            return
        if command == 139:      ## 0x8b
            print( "GET_SET_MEMORY_POSITION_3 request received", command, hex(command), self.notifying )
            newVal = [0x01, 0x07, 0x01, 0xe1, 0x07, 0x8f, 0x87, 0x00, 0x00]
            self.notifyValue(newVal)
            return
        if command == 140:      ## 0x8c
            print( "GET_SET_MEMORY_POSITION_4 request received", command, hex(command), self.notifying )
            newVal = [0x01, 0x07, 0x01, 0xe1, 0x07, 0x8f, 0x87, 0x00, 0x00]
            self.notifyValue(newVal)
            return

        print( "Unknown DPG command code:", command, hex(command) )
