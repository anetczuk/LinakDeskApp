# Linak Desk Application
This is desktop application controlling Linak office desks. Application functionality is 
similar to application provided by Linak. 
One of the goals of this project is to allow the desk control under Linux operating 
systems, because official application does not support Linux OS. 

Application was tested on *DPG1C* desk panel containing built-in Bluetooth module.

Communication protocol between *DPG1C* module and official application was
reverse engineered mostly by mocking *DPG1C* Bluetooth service.


## Features
- scanning for nearby devices
- moving up/down
- moving to favourite position
- setting reminder, desk offset and favoritie positions
- system tray icon
- auto reconnecting to recent device
- persisting application settings
- drawing position chart over time
- position statistics


## Screens

[![Status of desk](doc/app-screen-status-small.png "Status of desk")](doc/app-screen-status-big.png)
[![Application settings](doc/app-screen-settings-small.png "Application settings")](doc/app-screen-settings-big.png)
[![Device settings](doc/app-screen-device-small.png "Device settings")](doc/app-screen-device-big.png)


## Modules
- linakdeskapp.main -- entry point for the application
- linakdeskmock -- Bluetooth service mocking Linak desk service
- testlinakdeskapp -- unit tests for the application


## Permissions

*Bluepy* package requires special privileges when scanning for nearby devices.
It is recomended to solve it by adding capabilities to the package:
`cd <PYTHON_PATH>/site-packages/bluepy
sudo setcap 'cap_net_raw,cap_net_admin+eip' bluepy-helper
`
Go to directory where bluepy is installed (local user or system) and execute `setcap` as stated above.


## Running application

To run application try one of:
- run *src/linakdeskctl*
- run *src/linakdeskapp/main.py* 
- execute *cd src; python3 -m linakdeskapp*

Application can be run in profiler mode passing *--profile* as command line parameter. 

Before first use make sure You have fetched *lib* submodule (see _Required libraries_ section).


### Running mock service

To run mock simply execute *linakdeskmock/main.py* file.


### Running tests

To run tests execute *src/testlinakdeskapp/runtests.py*. It can be run with code profiling 
and code coverage options.

In addition there is demo application not requiring Bluetooth connection. It 
can be run by *testlinakdeskapp/gui/main_window_example.py*.


## Required libraries
- PyQt5
- matplotlib
- pandas
- bluepy

Installation:
- `sudo apt install python3-pyqt5`
- `pip3 install -r ./src/requirements.txt`

Following instructions can be executed by once by script `./src/install_reqs.sh`

In addition, application requires additional submodule located in *lib* directory.
To fetch the module simply call *configure_submodules.sh* script placed in root directory tree.


## Working with venv

There are two scripts that make it easy to work with *venv*:
- `tools/installvenv.sh`
- `tools/startvenv.sh`

They prepare and start virtual environment respectively.

In addition following package is required (installed from within venv):
- `pip3 install --user vext.pyqt5`


## Examples of use of not obvious Python mechanisms:
- use of *EnumMeta* class (*linak_service.py*)
- defining method decorators (*synchronied.py*)
- use of threading: *Thread*, *Event*, *Timer*
- use of *QThreadPool* and *Worker* concepts
- properly killing (Ctrl+C) PyQt (*sigint.py*)
- loading of UI files and inheriting from it
- embedding matplotlib graph with navigation toolbar into PyQt widget
- code profiling (*cProfile*)
- code coverage (*coverage*)


## ToDo:
- handle cm/inch unit switch
- add fav buttons inside popup of system tray icon
- handle away from keyboard


## Issues:
- disabling light guidance does not seem to work. It seems to be problem on 
device side, because even in Linak app it does not work.


## Support

If You like the project or if it is valuable to You then feel free to support my work.

[![Donate with PayPal](https://www.paypalobjects.com/en_US/i/btn/btn_donate_LG.gif "Donate with PayPal")](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=EZZ5S8DE3RHW4&source=url)


## References:
- https://www.linak.com/products/controls/dpg-with-reminder/
- https://www.linak.com/products/controls/desk-control-apps/
- https://ianharvey.github.io/bluepy-doc/index.html
- https://github.com/Vudentz/BlueZ/tree/master/doc

