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


#### append local library
sys.path.append(os.path.abspath( os.path.join(os.path.dirname(__file__), "../..") ))


import argparse
import logging

import linakdeskapp.logger as logger

from linakdeskapp.gui.qt import QApplication
from linakdeskapp.gui.sigint import setup_interrupt_handling
from linakdeskapp.gui.main_window import MainWindow

from testlinakdeskapp.gui.device_connector_mock import DeviceConnectorMock


## ============================= main section ===================================


if __name__ != '__main__':
    sys.exit(0)

parser = argparse.ArgumentParser(description='Linak desk application')
parser.add_argument('--profile', action='store_const', const=True, default=False, help='Profile the code' )
parser.add_argument('--pfile', action='store', default=None, help='Profile the code and output data to file' )
# parser.add_argument('--mode', action='store', required=True, choices=["BF", "POLY", "COMMON"], help='Mode' )
# parser.add_argument('--file', action='store', required=True, help='File with data' )
parser.add_argument('--connect', action='store', default=None, help='BT address to connect to' )
parser.add_argument('--minimized', action='store_const', const=True, default=False, help='Start minimized' )


args = parser.parse_args()


logFile = logger.get_logging_output_file()
logger.configure( logFile )


_LOGGER = logging.getLogger(__name__)

_LOGGER.debug("\n\n")
_LOGGER.debug("Starting the test application")

_LOGGER.debug("Logger log file: %s" % logFile)


exitCode = 0

try:

    app = QApplication(sys.argv)
    app.setApplicationName("LinakDeskApp")
    app.setOrganizationName("arnet")
    ### app.setOrganizationDomain("www.my-org.com")

    window = MainWindow()
    window.loadSettings()

    connector = DeviceConnectorMock()

    window.attachConnector(connector, args.connect)

    if args.minimized is False:
        window.show()

    setup_interrupt_handling()

    exitCode = app.exec_()

    if exitCode == 0:
        window.saveSettings()

    _LOGGER.info("Done with exit code: %s", exitCode)

except BaseException:
    exitCode = 1
    _LOGGER.exception("Exception occurred")
    raise

sys.exit(exitCode)
