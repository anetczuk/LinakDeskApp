#!/usr/bin/python2
#
#
# Code based on:
#        https://github.com/Vudentz/BlueZ/blob/master/test/example-gatt-server
#        https://github.com/Vudentz/BlueZ/blob/master/test/example-advertisement
#

import sys
import os

# sys.path.append(os.path.abspath( os.path.join(os.path.dirname(__file__), "..") ))
# sys.path.append(os.path.abspath( os.path.join(os.path.dirname(__file__), "../../lib") ))
sys.path.append(os.path.abspath( os.path.join(os.path.dirname(__file__), "../../lib/linak_bt_desk") ))

import gobject
import dbus.mainloop.glib

from advertisement import TestAdvertisement
from service.service import DBUS_OM_IFACE, DBUS_PROP_IFACE

from service.service import Service
# from service.genericaccessservice import GenericAccessService
from service.refinputservice import ReferenceInputService
from service.refoutputservice import ReferenceOutputService
from service.controlservice import ControlService
from service.dpgservice import DpgService
# from service.heartservice import HeartRateService
# from service.batteryservice import BatteryService
# from service.testservice import TestService


mainloop = None


BLUEZ_SERVICE_NAME              = 'org.bluez'
GATT_MANAGER_IFACE              = 'org.bluez.GattManager1'
LE_ADVERTISING_MANAGER_IFACE    = 'org.bluez.LEAdvertisingManager1'


def register_service_cb():
    print('GATT service registered')


def register_service_error_cb(error):
    print('Failed to register service: ' + str(error))
    mainloop.quit()


def find_gatt_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.iteritems():
        if GATT_MANAGER_IFACE in props:
            return o

    return None


def register_ad_cb():
    print( 'Advertisement registered' )


def register_ad_error_cb(error):
    print( 'Failed to register advertisement: ' + str(error) )
    mainloop.quit()


def find_advertise_adapter(bus):
    remote_om = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, '/'),
                               DBUS_OM_IFACE)
    objects = remote_om.GetManagedObjects()

    for o, props in objects.iteritems():
        if LE_ADVERTISING_MANAGER_IFACE in props:
            return o

    return None


def main():
    global mainloop

    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()

    advertise_adapter = find_advertise_adapter(bus)
    if not advertise_adapter:
        print('LEAdvertisingManager1 interface not found')
        return

    gatt_adapter = find_gatt_adapter(bus)
    if not gatt_adapter:
        print('GattManager1 interface not found')
        return

    adapter_props = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, advertise_adapter),
                                   DBUS_PROP_IFACE)

    adapter_props.Set("org.bluez.Adapter1", "Powered", dbus.Boolean(1))

    ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, advertise_adapter),
                                LE_ADVERTISING_MANAGER_IFACE)

    test_advertisement = TestAdvertisement(bus, 0)

    service_manager = dbus.Interface(
            bus.get_object(BLUEZ_SERVICE_NAME, gatt_adapter),
            GATT_MANAGER_IFACE)

    mainloop = gobject.MainLoop()

    ad_manager.RegisterAdvertisement(test_advertisement.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)

    Service.register_service( service_manager, ControlService(bus, 0) )
    Service.register_service( service_manager, DpgService(bus, 1) )
    Service.register_service( service_manager, ReferenceOutputService(bus, 2) )    ## mask
    Service.register_service( service_manager, ReferenceInputService(bus, 3) )

    mainloop.run()


if __name__ == '__main__':
    main()

