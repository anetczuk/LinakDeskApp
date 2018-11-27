"""
Handling Ctrl+C inside PyQt.

The code is taken from:
               https://coldfix.eu/2016/11/08/pyqt-boilerplate/

As stated on the website (https://coldfix.eu/about/), content and source code
is published under CC BY and CC0 license respectively.
"""


import signal
import logging

from .qt import QtCore, QApplication


_LOGGER = logging.getLogger(__name__)


# Define this as a global function to make sure it is not garbage
# collected when going out of scope:
def _interrupt_handler(signum, frame):
    """Handle KeyboardInterrupt: quit application."""
    _LOGGER.debug("Interrupt received: %s", signum)
    QApplication.exit(2)


def safe_timer(timeout, func, *args, **kwargs):
    """
    Create a timer that is safe against garbage collection and overlapping calls.

    See: http://ralsina.me/weblog/posts/BB974.html
    """
    def timer_event():
        try:
            func(*args, **kwargs)
        finally:
            QtCore.QTimer.singleShot(timeout, timer_event)

    QtCore.QTimer.singleShot(timeout, timer_event)


# Call this function in your main after creating the QApplication
def setup_interrupt_handling():
    """Set up handling of KeyboardInterrupt (Ctrl-C) for PyQt."""
    signal.signal(signal.SIGINT, _interrupt_handler)
    # Regularly run some (any) python code, so the signal handler gets a
    # chance to be executed:
    safe_timer(100, lambda: None)
