"""This script captures video from a camera and displays it in grayscale"""

import sys

import cv2 as cv
from PyQt5.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget

from vigil.pixel_view import PixelView
from vigil.splash_window import VigilSplashWindow

VIRAT_PATH = "/home/lucaskeller/code/cv/vigil/videos/v"
VIRAT_FILETYPE = ".mpg"


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

        central_widget.setLayout(grid)
        self.setCentralWidget(central_widget)


def main():
    """
    Initializes a GUI window with four video streams from VIRAT dataset.
    """
    app = QApplication([])

    splash = launch_splash()

    main_window = MainWindow()
    main_window.show()
    splash.finish(main_window)

    sys.exit(app.exec())


def launch_splash():
    """Launches the VigilSplashWindow and shows it to the user."""
    splash = VigilSplashWindow()
    splash.show()
    splash.progress()
    return splash


if __name__ == "__main__":
    main()