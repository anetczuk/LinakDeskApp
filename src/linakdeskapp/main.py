#!/usr/bin/python3
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


import sys
import os
# import signal
# from time import sleep

#### append local library
script_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath( os.path.join(script_dir, "..") ))
sys.path.append(os.path.abspath( os.path.join(script_dir, "../../lib/linak_bt_desk") ))

import time
import argparse
import logging
import cProfile

import linakdeskapp.logger as logger

from linakdeskapp.gui.main_window import MainWindow

from linakdeskapp.bt_device_connector import BTDeviceConnector
from linakdeskapp.bt_device_object import BTDeviceObject
from linakdeskapp.gui.qt import QApplication
from linakdeskapp.gui.sigint import setup_interrupt_handling 



logger.configure()
_LOGGER = logging.getLogger(__name__)



def runApp(args):
    if args.scan == True:
        _LOGGER.info( "Scanning for BT devices" )
        btConnector = BTDeviceConnector()
        devices = btConnector.scanDevices()
        if len(devices) < 1:
            _LOGGER.info( "No BT devices found" )
        else:
            for dev in devices:
                _LOGGER.info( "Found device: %s", dev )  
        return 0  

    if args.desc == True:
        BTDeviceObject.printDescription( args.connect )
        return 0

    ## GUI
    app = QApplication(sys.argv)
    app.setApplicationName("LinakDeskApp")
    app.setOrganizationName("arnet")
    ### app.setOrganizationDomain("www.my-org.com")
                  
    window = MainWindow()
    window.loadSettings()
    
    btConnector = BTDeviceConnector()
    window.attachConnector(btConnector)
    
    if args.connect != None:
        btAddress = args.connect
        btConnector.connectTo( btAddress )        
         
    if args.minimized == False:
        window.show()
     
    setup_interrupt_handling()
     
    exitCode = app.exec_()

    if exitCode == 0:
        window.saveSettings()
    
    return exitCode


def main():
    parser = argparse.ArgumentParser(description='Linak desk application')
    parser.add_argument('--profile', action='store_const', const=True, default=False, help='Profile the code' )
    parser.add_argument('--pfile', action='store', default=None, help='Profile the code and output data to file' )
    parser.add_argument('--connect', action='store', default=None, help='BT address to connect to' )
    parser.add_argument('--desc', action='store_const', const=True, default=False, help='Print description of connected BT and exit' )
    parser.add_argument('--scan', action='store_const', const=True, default=False, help='Scan nearby BT devices' )
    parser.add_argument('--minimized', action='store_const', const=True, default=False, help='Start minimized' )
     
          
    args = parser.parse_args()

    
    _LOGGER.debug("\n\n")
    _LOGGER.debug("Starting the application")
    
    _LOGGER.debug("Logger log file: %s" % logger.log_file)
    
    
    
    starttime = time.time()
    profiler = None
    
    exitCode = 0
    
    
    try:
     
        profiler_outfile = args.pfile
        if args.profile == True or profiler_outfile != None:
            print( "Starting profiler" )
            profiler = cProfile.Profile()
            profiler.enable()
    
    
        exitCode = runApp(args)
    
    
    # except BluetoothError as e:
    #     print "Error: ", e, " check if BT is powered on"
    
    except:
        exitCode = 1
        _LOGGER.exception("Exception occured")
        raise
    
    finally:
        _LOGGER.info( "" )                    ## print new line
        if profiler != None:
            profiler.disable()
            if profiler_outfile == None:
                _LOGGER.info( "Generating profiler data" )
                profiler.print_stats(1)
            else:
                _LOGGER.info( "Storing profiler data to", profiler_outfile )
                profiler.dump_stats( profiler_outfile )
                _LOGGER.info( "pyprof2calltree -k -i", profiler_outfile )
             
        timeDiff = (time.time()-starttime)*1000.0
        _LOGGER.info( "Calculation time: {:13.8f}ms".format(timeDiff) )
        
        sys.exit(exitCode)


if __name__ == '__main__':
    main()
