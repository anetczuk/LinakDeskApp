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
import signal
from time import sleep

#### append local library
sys.path.append(os.path.abspath( os.path.join(os.path.dirname(__file__), "..") ))
sys.path.append(os.path.abspath( os.path.join(os.path.dirname(__file__), "../../lib/linak_bt_desk") ))

import time
import argparse
import logging
import cProfile
from bt_device_connector import BTDeviceConnector


try:
    from bluepy.btle import Scanner
except ImportError as e:
    ### No module named <name>
    print(e)
    exit(1)


from linak_dpg_bt.linak_device import LinakDesk

from linakdeskcontrol.gui.main_window import MainWindow
# from bt_device_connector import BTDeviceConnector


from gui.qt import QApplication

from gui.sigint import setup_interrupt_handling 



# def scanDevices():
#     if os.getuid() != 0:
#         print( "Functionality needs root privileges" )
#         exit(1)
#     
#     print( "Scanning bluetooth devices" )
#     
#     scanner = Scanner()
#     devices = scanner.scan(10.0)
#     
#     for dev in devices:
#         print( "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi) )
#         for (adtype, desc, value) in dev.getScanData():
#             print( "  %s = %s" % (desc, value) )



## ============================= main section ===================================


if __name__ != '__main__':
    sys.exit(0)


## pilot: DPG1C


parser = argparse.ArgumentParser(description='Linak desk controller')
parser.add_argument('--profile', action='store_const', const=True, default=False, help='Profile the code' )
parser.add_argument('--pfile', action='store', default=None, help='Profile the code and output data to file' )
# parser.add_argument('--mode', action='store', required=True, choices=["BF", "POLY", "COMMON"], help='Mode' )
# parser.add_argument('--file', action='store', required=True, help='File with data' )
# parser.add_argument('--mindsize', action='store', default=1, help='Minimal data size' )
 
  
  
args = parser.parse_args()


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)


search_time = 10


starttime = time.time()
profiler = None

exitCode = 0

try:
 
    profiler_outfile = args.pfile
    if args.profile == True or profiler_outfile != None:
        print( "Starting profiler" )
        profiler = cProfile.Profile()
        profiler.enable()


#     scanDevices()
    
    print( "Connecting" )


    
    def xxx(aaa, bbb):
        print("xxxxxx:", aaa, bbb, dir(bbb), bbb.__class__)
#         QApplication.closeAllWindows()
#         app.closeAllWindows()
#         print("fffff")
#         app.quit()
#         app.exit()
#         print("fffff2")
#     signal.signal(signal.SIGINT, xxx)            ## handles CTRL+C

#     signal.signal(signal.SIGINT, signal.SIG_DFL)            ## handles CTRL+C
#     signal.signal(signal.SIGINT, signal.SIG_IGN)            ## handles CTRL+C

        
#     def foo(aaa, bbb, ccc):
#         print( "xxccccccccccccc" )
#         ###raise KeyboardInterrupt()
#     
#     sys.excepthook = foo
    
    
    ## GUI
    app = QApplication(sys.argv)
        
    btConnector = BTDeviceConnector()
        
    window = MainWindow()
    window.attachConnector(btConnector)
        
    btConnector.connectTo("c6:e4:0a:57:2f:e0")
        
    window.show()
    
    setup_interrupt_handling()
    
    exitCode = app.exec_()

    
#     desk = LinakDesk("c6:e4:0a:57:2f:e0")
#      
#     print( "\nReading data" )
#      
#     desk.read_dpg_data()
#       
#     print( "Done" )
#        
#     print( "Name:", desk.name )
# #     print "Height:", desk.current_height_with_offset.human_cm
#     print( "State:", desk )
# 
#     print( "Moving" )
#     desk.move_to_cm(95)
    


#     dataParser = DataParser()
#     data = dataParser.parseFile(args.file)
# 
#     minSearchData = int(args.mindsize)
#     
#     if   args.mode == "BF":
#         ## finding full key by forward algorithm
#         finder = RevHwCRC(True)
# #         finder = RevDivisionCRC(True)
# #         finder = RevModCRC(True)
# #         finder = RevCRCCommon(True)
#         retList = finder.bruteForceInput(data, minSearchData)
#         if len(retList) < 1:
#             print "\nNo keys discovered"
#         else:
#             print "\nDiscovered keys[{:}]:".format( len(retList) )
#             for key in retList:
#                 print key
#     elif args.mode == "POLY":
#         ## find polygons by xor-ing data pairs
#         finder = RevHwCRC(True)
# #         finder = RevDivisionCRC(True)
# #         finder = RevModCRC(True)
# #         finder = RevCRCCommon(True)
#         retList = finder.findPolysInput(data, minSearchData)
#         if len(retList) < 1:
#             print "\nNo polys discovered"
#         else:
#             print "\nDiscovered polys[{:}]:".format( len(retList) )
#             for poly in retList.most_common():
#                 print poly[0], poly[1]
#     elif args.mode == "COMMON":
#         ## finding full key by backward algorithm
#         finder = RevHwCRC(True)
# #         finder = RevDivisionCRC(True)
# #         finder = RevModCRC(True)
# #         finder = RevCRCCommon(True)
#         retList = finder.findCommonInput(data, minSearchData)
#         if len(retList) < 1:
#             print "\nNo keys discovered"
#         else:
#             print "\nDiscovered keys[{:}]:".format( len(retList) )
#             for poly in retList.most_common():
#                 print poly[0], poly[1]
#     else:
#         print "Invalid mode:", args.mode
#         sys.exit(1)


# except BluetoothError as e:
#     print "Error: ", e, " check if BT is powered on"

finally:
    print( "" )                    ## print new line
    if profiler != None:
        profiler.disable()
        if profiler_outfile == None:
            print( "Generating profiler data" )
            profiler.print_stats(1)
        else:
            print( "Storing profiler data to", profiler_outfile )
            profiler.dump_stats( profiler_outfile )
            print( "pyprof2calltree -k -i", profiler_outfile )
         
    timeDiff = (time.time()-starttime)*1000.0
    print( "Calculation time: {:13.8f}ms".format(timeDiff) )
    
    sys.exit(exitCode)

