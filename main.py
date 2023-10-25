"""This script captures video from a camera and displays it in grayscale"""

import sys
from enum import Enum, auto

import cv2 as cv
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget

from vigil.generated_ui.vigil_controller import VigilControllerUI
from vigil.pixel_view import PixelView
from vigil.splash_window import VigilSplashWindow

VIRAT_PATH = "/home/lucaskeller/code/cv/vigil/videos/v"
VIRAT_FILETYPE = ".mpg"


class VigilStreamFocus(Enum):
    """
    An enumeration of the possible video streams that the user can focus on.
    """

    STREAM_1 = auto()
    STREAM_2 = auto()
    STREAM_3 = auto()
    STREAM_4 = auto()
    CONCURRENT = auto()


class VigilControllerWindow(QWidget):
    """
    A window that displays the VigilControllerUI and allows the user to interact with it.

    :param main_app: The main application object.
    """

    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app

        self.ui = VigilControllerUI()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.define_on_click()

    def define_on_click(self):
        """
        Connects the click events of the push buttons to the corresponding stream focus method of 
        the main app.
        """
        self.ui.pushButton.clicked.connect(
            lambda: self.main_app.focus_stream(VigilStreamFocus.STREAM_1)
        )
        self.ui.pushButton_2.clicked.connect(
            lambda: self.main_app.focus_stream(VigilStreamFocus.STREAM_2)
        )
        self.ui.pushButton_3.clicked.connect(
            lambda: self.main_app.focus_stream(VigilStreamFocus.STREAM_3)
        )
        self.ui.pushButton_4.clicked.connect(
            lambda: self.main_app.focus_stream(VigilStreamFocus.STREAM_4)
        )
        self.ui.pushButton_5.clicked.connect(
            lambda: self.main_app.focus_stream(VigilStreamFocus.CONCURRENT)
        )


class MainWindow(QMainWindow):
    """
    The main window of the VIGIL application.

    This window displays several video streams from the IRAT dataset
    using instances of the PixelView class.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("VIGIL")
        central_widget = QWidget()
        central_widget.setFixedSize(1920, 1080)

        grid = self.create_videocapture_grid()

        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)

    def create_videocapture_grid(self):
        """
        Creates and returns a grid of four video capture windows using
        cv.VideoCapture.
        """
        grid = QGridLayout()

        caps = [
            cv.VideoCapture(VIRAT_PATH + str(i) + VIRAT_FILETYPE) for i in range(1, 5)
        ]
        pix_windows = iter(
            [PixelView(cap, name="VIRAT_" + str(idx)) for idx, cap in enumerate(caps)]
        )
        grid.addWidget(next(pix_windows), 0, 0)
        grid.addWidget(next(pix_windows), 0, 1)
        grid.addWidget(next(pix_windows), 1, 0)
        grid.addWidget(next(pix_windows), 1, 1)

        return grid

    def center(self):
        """Centers the main window on the user's screen."""
        relative_geometry = self.frameGeometry()
        center_point = QApplication.desktop().availableGeometry().center()
        relative_geometry.moveCenter(center_point)
        self.move(relative_geometry.topLeft())

    def show(self):
        """Show main application in center of screen."""
        super().show()
        self.center()

    # pylint: disable=invalid-name
    def closeEvent(self, _):
        """Close all top-level windows when main window is closed.

        Note
            Implementation of https://doc.qt.io/qt-5/qwidget.html#closeEvent

        Args:
            _: The close event.
        """
        for widget in QApplication.topLevelWidgets():
            widget.close()

    def focus_stream(self, stream: VigilStreamFocus):
        """
        Focuses the main window on a particular video stream.

        :param stream: The video stream to focus on.
        """
        print(stream)
        if stream == VigilStreamFocus.CONCURRENT:
            print("Special, default case!")


def main():
    """
    Initializes a GUI window with four video streams from VIRAT dataset.
    """
    app = QApplication([])

    splash = launch_splash()

    main_window = MainWindow()
    main_window.show()
    splash.finish(main_window)

    controller_window = VigilControllerWindow(main_window)
    controller_window.show()

    sys.exit(app.exec())


def launch_splash():
    """Launches the VigilSplashWindow and shows it to the user."""
    splash = VigilSplashWindow()
    splash.show()
    splash.progress()
    return splash


if __name__ == "__main__":
    main()
