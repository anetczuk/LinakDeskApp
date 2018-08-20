##
##
##


try:
    from PyQt5 import QtCore
    from PyQt5.QtCore import QObject, pyqtSignal
    from PyQt5.QtWidgets import QApplication
#     from PyQt5 import uic
except ImportError as e:
    ### No module named <name>
    print(e)
    exit(1)
