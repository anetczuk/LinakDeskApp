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
import time

try:
    import daemon
except ImportError:
    print( "Missing coverage module. Try running 'pip install daemon'" )
    print( "Python info:", sys.version )
    raise
try:
    import lockfile
except ImportError:
    print( "Missing coverage module. Try running 'pip install lockfile'" )
    print( "Python info:", sys.version )
    raise


try:
    with daemon.DaemonContext(
            chroot_directory=None,
            working_directory='/tmp',
            pidfile=lockfile.FileLock('/var/run/linakdeskd.pid'),
            stdout=sys.stdout,
            stderr=sys.stderr
                              ):
#         while True:
        for _ in range(10):
            print( "Started" )
            print( os.getuid() )
            print( os.getgid() )
            print( os.getpid() )
            print( os.getcwd() )
            time.sleep(2)

except lockfile.LockFailed as e:
    print( "Lock file failed:", e )
    
finally:
    print( "Daemon died" )

