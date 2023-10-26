"""
This module primarily contains the VigilControllerWindow class, a window that displays 
the VigilControllerUI used to manage the vigil main window.
"""
from enum import IntEnum

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

from vigil.generated_ui.vigil_controller import VigilControllerUI


class VigilStreamFocus(IntEnum):
    """
    An enumeration of the possible video streams that the user can focus on.
    """

    STREAM_0 = 0
    STREAM_1 = 1
    STREAM_2 = 2
    STREAM_3 = 3
    CONCURRENT = 4


class VigilControllerWindow(QWidget):
    """
    A window that displays the VigilControllerUI and allows the user to interact with it.

    :param main_app: The main application object.
    """

    def __init__(self, main_app, screen=None):
        super().__init__()
        self.main_app = main_app

        self.ui = VigilControllerUI()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.define_on_click()

        q_rect = screen.geometry()
        self.move(q_rect.left(), q_rect.top())

    def define_on_click(self):
        """
        Connects the click events of the push buttons to the corresponding stream focus method of
        the main app.
        """
        self.ui.pushButton.clicked.connect(
            lambda: self.main_app.focus_stream(VigilStreamFocus.STREAM_0)
        )
        self.ui.pushButton_2.clicked.connect(
            lambda: self.main_app.focus_stream(VigilStreamFocus.STREAM_1)
        )
        self.ui.pushButton_3.clicked.connect(
            lambda: self.main_app.focus_stream(VigilStreamFocus.STREAM_2)
        )
        self.ui.pushButton_4.clicked.connect(
            lambda: self.main_app.focus_stream(VigilStreamFocus.STREAM_3)
        )
        self.ui.pushButton_5.clicked.connect(
            lambda: self.main_app.focus_stream(VigilStreamFocus.CONCURRENT)
        )
