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


# import pygtk, gtk
import gtk

# from DrawerWindow import DrawerWindow
# from ImageGrabber import ImageGrabberThread
# from ScreenSaverDisabler import ScreenSaverDisabler
# 
# import importlib
# import logging
# 
# import ntpath

##from provider.UrlProvider import ExampleProvider



# def import_module( path ):
#     moduleName = path.replace("/", ".")
#     className = ntpath.basename( path )
#     logging.info("importing module: %s %s", moduleName, className)
#     mod = importlib.import_module( moduleName )
#     return getattr(mod, className)


#
#
#
class MainWindow:
    def __init__(self):
        pass
#         self.imgWindow = DrawerWindow(fullscreen)
#         self.thread = ImageGrabberThread( self.imgWindow )
        ##self.thread.urlProvider = ExampleProvider()
        
#     def setProvider(self, provider):
#         self.thread.urlProvider = provider
        
#     def setDisplayTime(self, dTimeS):
#         self.thread.setDisplayTime( dTimeS )
        
    def main(self):
        print "Starting GUI"
#         self.thread.start()
#         gtk.gdk.threads_init()          ## run threads
        gtk.main()


