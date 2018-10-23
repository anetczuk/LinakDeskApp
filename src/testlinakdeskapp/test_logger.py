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


import unittest

import linakdeskapp.logger as logger

import logging
import io



class DeviceConnectorTest(unittest.TestCase):
    def setUp(self):
        ## Called before testfunction is executed
        self.logger = logging.Logger(__name__)
        self.logger.propagate = False
        self.logger.setLevel( logging.DEBUG )
        self.buffer = io.StringIO()
        handler = logging.StreamHandler( self.buffer )
        formatter = logger.createFormatter()
        handler.setFormatter( formatter )
        self.logger.addHandler( handler )
  
    def tearDown(self):
        ## Called after testfunction was executed
        self.logger = None
        self.buffer.close()
        self.buffer = None
       
    def test_emptyMessage(self):
        self.logger.info("")
        msg = self.buffer.getvalue()
        self.assertEqual(msg, "\n")
         
    def test_newLines_Linux(self):
        self.logger.info("\n\n\n")
        msg = self.buffer.getvalue()
        self.assertEqual(msg, "\n\n\n\n")
        
    def test_newLines_Windows(self):
        self.logger.info("\r\n\r\n\r\n")
        msg = self.buffer.getvalue()
        self.assertEqual(msg, "\r\n\r\n\r\n\n")
    