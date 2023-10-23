"""This script captures video from a camera and displays it in grayscale"""

import sys
import time

import cv2 as cv
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QApplication,
    QGraphicsScene,
    QGraphicsView,
    QGridLayout,
    QLabel,
    QSplashScreen,
    QVBoxLayout,
    QWidget,
)

from generated_ui.splash import SplashUI

VIRAT_PATH = "/home/lucaskeller/code/cv/vigil/videos/v"
VIRAT_FILETYPE = ".mpg"


class SplashScreen(QSplashScreen):
    """A custom splash screen widget with a progress bar for the Vigil application."""

    def __init__(self):
        super(QSplashScreen, self).__init__()

        self.ui = SplashUI()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        pixmap = QPixmap("images/splash_grad.png")
        self.setPixmap(pixmap)

    def progress(self):
        """
        Iteratively updates the progress bar on the user interface.
        """
        for i in range(101):
            time.sleep(0.01)
            self.ui.progress_bar.setValue(i)
            QApplication.processEvents()


class PixelWindow(QWidget):
    """
    A widget that displays a live video feed from a cv.VideoCapture object.

    Args:
        video_capture (cv.VideoCapture): The video capture object to extract frames from.
        name (str): The name to display above the video feed.
        fps (int, optional): The desired frames per second to display. Defaults to 30.
    """

    def __init__(self, video_capture: cv.VideoCapture, name, fps=30):
        super().__init__()
        self.video_capture = video_capture
        self.dimensions = (
            int(self.video_capture.get(cv.CAP_PROP_FRAME_WIDTH)),
            int(self.video_capture.get(cv.CAP_PROP_FRAME_HEIGHT)),
        )

        self.setup_gui(name)
        self.continuously_refresh(fps)

    def continuously_refresh(self, fps):
        """
        Sets up a QTimer to continuously refresh the video feed at the desired frames per second.

        Args:
            fps (int): The desired frames per second to display.
        """
        timer = QTimer(self)
        period_ms = int(1000 / fps)
        timer.setInterval(period_ms)
        timer.timeout.connect(self.extract_cv2_frame_to_pixmap)
        timer.start()

    def setup_gui(self, name):
        """
        Sets up the GUI elements for the widget.

        Args:
            name (str): The name to display above the video feed.
        """
        scene = QGraphicsScene()
        pixmap = QPixmap(*self.dimensions)
        self.pixmap_item = scene.addPixmap(pixmap)

        view = QGraphicsView(self)
        view.setScene(scene)
        view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        text = QLabel(name, self)

        stack_layout = QVBoxLayout(self)
        stack_layout.addWidget(text)
        stack_layout.addWidget(view)

    def __del__(self):
        """
        Releases the video capture object when the widget is deleted.
        """
        self.video_capture.release()

    def extract_cv2_frame_to_pixmap(self):
        """
        Extracts a frame from the video capture object and displays it in the widget.
        """
        _, frame = self.video_capture.read()
        image = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.pixmap_item.setPixmap(pixmap)


def main():
    """
    Initializes a GUI window with four video streams from VIRAT dataset.
    """
    app = QApplication([])

    splash = SplashScreen()
    splash.show()
    splash.progress()

    window = QWidget()
    grid = QGridLayout()

    caps = [cv.VideoCapture(VIRAT_PATH + str(i) + VIRAT_FILETYPE) for i in range(1, 5)]
    pix_windows = iter(
        [PixelWindow(cap, name="VIRAT_" + str(idx)) for idx, cap in enumerate(caps)]
    )
    grid.addWidget(next(pix_windows), 0, 0)
    grid.addWidget(next(pix_windows), 0, 1)
    grid.addWidget(next(pix_windows), 1, 0)
    grid.addWidget(next(pix_windows), 1, 1)

    window.setLayout(grid)
    window.show()

    splash.finish(window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
