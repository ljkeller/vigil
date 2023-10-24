"""Implements a widget that displays a video feed from a cv.VideoCapture object."""

import cv2 as cv
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QLabel, QVBoxLayout, QWidget


class PixelView(QWidget):
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
