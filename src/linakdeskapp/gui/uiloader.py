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

import logging


try:
    from PyQt5 import uic
except ImportError as e:
    ### No module named <name>
    logging.exception("Exception while importing")
    exit(1)    

import linakdeskapp.defs as defs


def generateUIFileNameFromClassName(classFileName):
    baseName = os.path.basename(classFileName)
    nameTuple = os.path.splitext(baseName)
    return nameTuple[0] + ".ui"


def loadUi(uiFilename):
    try:
        return uic.loadUiType( os.path.join( defs.ROOT_DIR, "ui", uiFilename ) )
    except Exception as e:
        print("Exception while loading UI file:", uiFilename, e)
        raise


def loadUiFromClassName(uiFilename):
    ui_file = generateUIFileNameFromClassName(uiFilename)
    return loadUi( ui_file )

