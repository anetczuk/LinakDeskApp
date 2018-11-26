#
# Code based on:
#        https://github.com/Vudentz/BlueZ/blob/master/test/example-gatt-server
#        https://github.com/Vudentz/BlueZ/blob/master/test/example-advertisement
#

import logging

import dbus.service
import gobject

from exception import *



DBUS_OM_IFACE =      'org.freedesktop.DBus.ObjectManager'
DBUS_PROP_IFACE =    'org.freedesktop.DBus.Properties'

GATT_SERVICE_IFACE = 'org.bluez.GattService1'
GATT_CHRC_IFACE =    'org.bluez.GattCharacteristic1'
GATT_DESC_IFACE =    'org.bluez.GattDescriptor1'



class Service(dbus.service.Object):
    PATH_BASE = '/org/bluez/example/service'

    def __init__(self, bus, index, uuid, primary):
        self.path = self.PATH_BASE + str(index)
        self.bus = bus
        self.uuid = uuid
        self.primary = primary
        self.characteristics = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        props = {
                GATT_SERVICE_IFACE: {
                        'UUID': self.uuid,
                        'Primary': self.primary,
                        'Characteristics': dbus.Array(
                                self.get_characteristic_paths(),
                                signature='o')
                }
        }
#         print( "returning props:", props )
        return props

    def get_path(self):
        path = dbus.ObjectPath(self.path)
#         print( "returning path:", path )
        return path

    def add_characteristic(self, characteristic):
        self.characteristics.append(characteristic)

    def get_characteristic_paths(self):
        result = []
        for chrc in self.characteristics:
            result.append(chrc.get_path())
#         print( "returning char paths:", result )
        return result

    def get_characteristics(self):
#         print( "returning chars:", self.characteristics )
        return self.characteristics

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_SERVICE_IFACE:
            raise InvalidArgsException()

        allprops = self.get_properties[GATT_SERVICE_IFACE]
#         print( "returning all props:", allprops )
        return allprops

    @dbus.service.method(DBUS_OM_IFACE, out_signature='a{oa{sa{sv}}}')
    def GetManagedObjects(self):
        response = {}
#         print('GetManagedObjects')

        response[self.get_path()] = self.get_properties()
        chrcs = self.get_characteristics()
        for chrc in chrcs:
            response[chrc.get_path()] = chrc.get_properties()
            descs = chrc.get_descriptors()
            for desc in descs:
                response[desc.get_path()] = desc.get_properties()
#         print( "returning objects:", response )
        return response

    def register(self, manager):
        manager.RegisterService(self.get_path(), {},
                                reply_handler=self._register_service_cb,
                                error_handler=self._register_service_error_cb)

    @classmethod
    def register_service(cls, manager, service):
        service.register(manager)

    def _register_service_cb(self):
        print('GATT service registered: %s' % (self.__class__.__name__))

    def _register_service_error_cb(self, error):
        print('Failed to register service: ' + str(error))


class Characteristic(dbus.service.Object):
    def __init__(self, bus, index, uuid, flags, service):
        self.path = service.path + '/char' + str(index)
        self.bus = bus
        self.uuid = uuid
        self.service = service
        self.flags = flags
        self.descriptors = []
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        props = {
                GATT_CHRC_IFACE: {
                        'Service': self.service.get_path(),
                        'UUID': self.uuid,
                        'Flags': self.flags,
                        'Descriptors': dbus.Array(
                                self.get_descriptor_paths(),
                                signature='o')
                }
        }
#         print( "returning props:", props )
        return props

    def get_path(self):
        path = dbus.ObjectPath(self.path)
#         print( "returning path:", path )
        return path

    def add_descriptor(self, descriptor):
        self.descriptors.append(descriptor)

    def get_descriptor_paths(self):
        result = []
        for desc in self.descriptors:
            result.append(desc.get_path())
#         print( "returning paths:", result )
        return result

    def get_descriptors(self):
        return self.descriptors

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_CHRC_IFACE:
            raise InvalidArgsException()

        props = self.get_properties[GATT_CHRC_IFACE]
#         print( "returning props:", props )
        return props

    ### called on read request from connected device
    @dbus.service.method(GATT_CHRC_IFACE, out_signature='ay')
    def ReadValue(self):
        try:
            value = self.readValueHandler()
            wrapped = self._wrap(value)
            print self.__class__.__name__, "sending data:", repr(value), "->", repr(wrapped)
            return wrapped
        except:
            logging.exception("Exception occured")
            raise

    ### called when connected device send something to characteristic
    @dbus.service.method(GATT_CHRC_IFACE, in_signature='ay')
    def WriteValue(self, value):
        try:
            unwrapped = self._unwrap(value)
            print self.__class__.__name__, "received data:", repr(value), "->", repr(unwrapped), [hex(no) for no in unwrapped]
            self.writeValueHandler(unwrapped)
        except:
            logging.exception("Exception occured")
            raise

    def _wrap(self, value):
        ##return dbus.Array( value, dbus.Signature('ay') )
        if isinstance(value, list):
            vallist = []
            for x in value:
                vallist = vallist + self._wrap(x)
            return dbus.Array( vallist )
        if isinstance(value, int):
            return dbus.Array( [dbus.Byte( int(value) )] )
        print('Unsupported type:', repr(value))
        return None

    def _unwrap(self, value):
        if isinstance(value, dbus.Array):
            vallist = [self._unwrap(x) for x in value]
            return vallist
        if isinstance(value, dbus.Byte):
            return int(value)
        print 'Unsupported type:', repr(value)
        return None

    @dbus.service.method(GATT_CHRC_IFACE)
    def StartNotify(self):
        try:
            self.startNotifyHandler()
        except:
            logging.exception("Exception occured")
            raise

    @dbus.service.method(GATT_CHRC_IFACE)
    def StopNotify(self):
        try:
            self.stopNotifyHandler()
        except:
            logging.exception("Exception occured")
            raise

    def readValueHandler(self):
        print('Default ReadValue called, returning error')
        raise NotSupportedException()

    def writeValueHandler(self, value):
        print('Default WriteValue called, returning error')
        raise NotSupportedException()

    def startNotifyHandler(self):
        print('Default StartNotify called, returning error')
        raise NotSupportedException()

    def stopNotifyHandler(self):
        print('Default StopNotify called, returning error')
        raise NotSupportedException()

    @dbus.service.signal(DBUS_PROP_IFACE, signature='sa{sv}as')
    def PropertiesChanged(self, interface, changed, invalidated):
        pass



class RCharacteristic(Characteristic):

    def __init__(self, bus, index, uuid, service):
        Characteristic.__init__(
                self, bus, index,
                uuid,
                ['read'],
                service)
        self.value_lvl = 100

    def readValueHandler(self):
        return self.value_lvl


class RWCharacteristic(Characteristic):

    def __init__(self, bus, index, uuid, service):
        Characteristic.__init__(
                self, bus, index,
                uuid,
                ['read', 'write'],
                service)
        self.value_lvl = 100

    def readValueHandler(self):
        return self.value_lvl

    def writeValueHandler(self, value):
        self.value_lvl = value


class RNCharacteristic(Characteristic):

    def __init__(self, bus, index, uuid, service):
        Characteristic.__init__(
                self, bus, index,
                uuid,
                ['read', 'notify'],
                service)
        self.notifying = False
        self.value_lvl = 100
        gobject.timeout_add(5000, self.change_value)

    def notify(self):
        if not self.notifying:
            return
        message = { 'Value': [dbus.ByteArray(self.value_lvl)] }
        self.PropertiesChanged(GATT_CHRC_IFACE, message, [])

    def change_value(self):
        if self.value_lvl > 0:
            self.value_lvl -= 2
            if self.value_lvl < 0:
                self.value_lvl = 0
        self.notify()
        return True

    def readValueHandler(self):
        return self.value_lvl

    def startNotifyHandler(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        print 'Starting notifying', self.__class__.__name__
        self.notifying = True
        self.notify()

    def stopNotifyHandler(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        print 'Stopping notifying', self.__class__.__name__
        self.notifying = False


class WWCharacteristic(Characteristic):

    def __init__(self, bus, index, uuid, service):
        Characteristic.__init__(
                self, bus, index,
                uuid,
                ['write-without-response', 'write'],
                service)
        self.value_lvl = 100

    def readValueHandler(self):
        return self.value_lvl

    def writeValueHandler(self, value):
        self.value_lvl = value


class RWWNCharacteristic(Characteristic):

    def __init__(self, bus, index, uuid, service):
        Characteristic.__init__(
                self, bus, index,
                uuid,
                ['read', 'write-without-response', 'write', 'notify'],
                service)
        self.notifying = False
        self.value_lvl = 100
#         gobject.timeout_add(5000, self.change_value)

    def notifyValue(self, value):
        self.value_lvl = value
        self.notify()

    def notify(self):
        if not self.notifying:
            return
        wrapped = self._wrap(self.value_lvl)
        message = { 'Value': wrapped }
        print self.__class__.__name__, 'notify:', self.value_lvl
        self.PropertiesChanged(GATT_CHRC_IFACE, message, [])

    def readValueHandler(self):
        return self.value_lvl

    def writeValueHandler(self, value):
        self.value_lvl = value

    def startNotifyHandler(self):
        if self.notifying:
            print('Already notifying, nothing to do')
            return

        print 'Starting notifying', self.__class__.__name__
        self.notifying = True

    def stopNotifyHandler(self):
        if not self.notifying:
            print('Not notifying, nothing to do')
            return

        print 'Stopping notifying', self.__class__.__name__
        self.notifying = False


class Descriptor(dbus.service.Object):
    def __init__(self, bus, index, uuid, flags, characteristic):
        self.path = characteristic.path + '/desc' + str(index)
        self.bus = bus
        self.uuid = uuid
        self.flags = flags
        self.chrc = characteristic
        dbus.service.Object.__init__(self, bus, self.path)

    def get_properties(self):
        return {
                GATT_DESC_IFACE: {
                        'Characteristic': self.chrc.get_path(),
                        'UUID': self.uuid,
                        'Flags': self.flags,
                }
        }

    def get_path(self):
        return dbus.ObjectPath(self.path)

    @dbus.service.method(DBUS_PROP_IFACE,
                         in_signature='s',
                         out_signature='a{sv}')
    def GetAll(self, interface):
        if interface != GATT_DESC_IFACE:
            raise InvalidArgsException()

        return self.get_properties[GATT_CHRC_IFACE]

    @dbus.service.method(GATT_DESC_IFACE, out_signature='ay')
    def ReadValue(self):
        print ('Default ReadValue called, returning error')
        raise NotSupportedException()

    @dbus.service.method(GATT_DESC_IFACE, in_signature='ay')
    def WriteValue(self, value):
        print('Default WriteValue called, returning error')
        raise NotSupportedException()

