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

import os
import sys
import logging



script_dir = os.path.dirname(__file__)



def getLoggingOutputFile():
    logDir = os.path.join(script_dir, "../../tmp")
    if os.path.isdir( logDir ) == False:
        logDir = os.getcwd()
        
    logFile = os.path.join(logDir, "log.txt")
    return logFile


def configure( logFile ):
    # logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    
    loggerFormat = '%(asctime)s,%(msecs)-3d %(levelname)-8s %(threadName)s [%(filename)s:%(lineno)d] %(message)s'
    
    # logging.basicConfig( stream = sys.stdout, 
    #                      format = loggerFormat,
    #                      datefmt = '%H:%M:%S', 
    #                      level = logging.DEBUG )
    
    logging.basicConfig( format = loggerFormat,
                         datefmt = '%Y-%m-%d %H:%M:%S', 
                         level = logging.DEBUG,
                         handlers=[ logging.FileHandler( filename = logFile, mode = "a+" ),
                                    logging.StreamHandler( stream = sys.stdout )]
                         )
