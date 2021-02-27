# MIT License
#
# Copyright (c) 2020 Arkadiusz Netczuk <dev.arnet@gmail.com>
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

import os
import sys
import logging
import logging.handlers as handlers


script_dir = os.path.dirname(__file__)
log_file = None


def get_logging_output_file():
    logDir = os.path.join(script_dir, "../../tmp/log")
    logDir = os.path.abspath( logDir )
    os.makedirs( logDir, exist_ok=True )
    if os.path.isdir( logDir ) is False:
        ## something bad happened (or unable to create directory)
        logDir = os.getcwd()

    logFile = os.path.join(logDir, "log.txt")
    return logFile


def configure( logFile=None, logLevel=None ):
    # pylint: disable=W0603
    global log_file

    log_file = logFile
    if log_file is None:
        log_file = get_logging_output_file()

    if logLevel is None:
        logLevel = logging.DEBUG

    ## rotation of log files, 1048576 equals to 1MB
    fileHandler    = handlers.RotatingFileHandler( filename=log_file, mode="a+", maxBytes=1048576, backupCount=999 )
    ## fileHandler    = logging.FileHandler( filename=log_file, mode="a+" )
    consoleHandler = logging.StreamHandler( stream=sys.stdout )

    formatter = create_formatter()

    fileHandler.setFormatter( formatter )
    consoleHandler.setFormatter( formatter )

    logging.root.addHandler( consoleHandler )
    logging.root.addHandler( fileHandler )
    logging.root.setLevel( logLevel )

    logging.getLogger('matplotlib').setLevel(logging.WARNING)

##     loggerFormat   = '%(asctime)s,%(msecs)-3d %(levelname)-8s %(threadName)s [%(filename)s:%(lineno)d] %(message)s'
##     dateFormat     = '%Y-%m-%d %H:%M:%S'
##     logging.basicConfig( format   = loggerFormat,
##                          datefmt  = dateFormat,
##                          level    = logging.DEBUG,
##                          handlers = [ fileHandler, consoleHandler ]
##                        )


def configure_console( logLevel=None ):
    if logLevel is None:
        logLevel = logging.DEBUG

    consoleHandler = logging.StreamHandler( stream=sys.stdout )

    formatter = create_formatter()

    consoleHandler.setFormatter( formatter )

    logging.root.addHandler( consoleHandler )
    logging.root.setLevel( logLevel )


def create_stdout_handler():
    formatter = create_formatter()
    consoleHandler = logging.StreamHandler( stream=sys.stdout )
    consoleHandler.setFormatter( formatter )
    return consoleHandler


def create_formatter(loggerFormat=None):
    if loggerFormat is None:
        ## loggerFormat = '%(asctime)s,%(msecs)-3d %(levelname)-8s %(threadName)s [%(filename)s:%(lineno)d] %(message)s'
        loggerFormat = ('%(asctime)s,%(msecs)-3d %(levelname)-8s %(threadName)s %(name)s:%(funcName)s '
                        '[%(filename)s:%(lineno)d] %(message)s')
    dateFormat = '%Y-%m-%d %H:%M:%S'
    return EmptyLineFormatter( loggerFormat, dateFormat )
    ## return logging.Formatter( loggerFormat, dateFormat )


class EmptyLineFormatter(logging.Formatter):
    """Special formatter storing empty lines without formatting."""

    ## override base class method
    def format(self, record):
        msg = record.getMessage()
        clearMsg = msg.replace('\n', '')
        clearMsg = clearMsg.replace('\r', '')
        if not clearMsg:
            # empty
            return msg
        return super().format( record )
