"""Implements a widget that displays a video feed from a cv.VideoCapture object."""

import cv2 as cv
import numpy as np
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QLabel, QVBoxLayout, QWidget

# Assuming 1080p is the maximum resolution of the stream. This application
# targets 1080p monitors and cameras of resolution <= 1080p.
UPSCALE_DIMENSIONS = (1920, 1080)


class PeopleDetector:
    """
    A class that detects people in images using a Histogram of Oriented Gradients (HOG) algorithm.

    Attributes:
    -----------
    hog : cv2.HOGDescriptor
        The HOG descriptor used for detecting people.
    """

    def __init__(self):
        self.hog = cv.HOGDescriptor()
        self.hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())

    def detect_and_bound_people(self, frame, min_confidence=0.75):
        """
        Detects people in a given frame using a Histogram of Oriented Gradients (HOG) algorithm,
        and draws bounding boxes around them.

        Parameters:
        -----------
        frame : numpy.ndarray
            The input image frame to detect people in.
        min_confidence : float, optional
            The minimum confidence threshold for a detected person to be considered valid.
            Defaults to 0.75... OpenCV documentation doesnt specify what the max confidence
            value is, but I've seen weights > 1.0

        Returns:
        --------
        None
        """

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        boxes, weights = self.hog.detectMultiScale(gray, winStride=(8, 8))

        boxes = np.array([[x, y, x + w, y + h] for (x, y, w, h) in boxes])
        for (x1, y1, x2, y2), weight in zip(boxes, weights):
            if weight > min_confidence:
                cv.rectangle(frame, (x1, y1), (x2, y2), (65, 195, 99), 2)


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
        self.people_detector = PeopleDetector()
        self.upscale = False
        self.dimensions = (
            int(self.video_capture.get(cv.CAP_PROP_FRAME_WIDTH)),
            int(self.video_capture.get(cv.CAP_PROP_FRAME_HEIGHT)),
        )

        self.setup_gui(name)
        self.timer = self.setup_continuos_streaming(fps)

    def setup_continuos_streaming(self, fps):
        """
        Sets up a continuous streaming of frames from the camera to the GUI at the specified
        frames per second.

        Args:
            fps (int): The desired frames per second for the streaming.

        Returns:
            QTimer: The timer object used to control the streaming.
        """
        timer = QTimer(self)
        timer.timeout.connect(self.extract_cv2_frame_to_pixmap)

        period_ms = int(1000 / fps)
        timer.setInterval(period_ms)
        timer.start()

        return timer

    def continuously_refresh(self, fps):
        """
        Sets up a QTimer to continuously refresh the video feed at the desired frames per second.

        Args:
            fps (int): The desired frames per second to display.
        """
        if fps > 0:
            self.timer.start()
        else:
            self.timer.stop()

    def setup_gui(self, name):
        """
        Sets up the GUI elements for the widget.

        Args:
            name (str): The name to display above the video feed.
        """
        scene = QGraphicsScene()
        pixmap = QPixmap(*self.dimensions)
        self.pixmap_item = scene.addPixmap(pixmap)

        self.pix_graphics_view = QGraphicsView(self)
        self.pix_graphics_view.setScene(scene)
        self.pix_graphics_view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.pix_graphics_view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        text = QLabel(name, self)

        stack_layout = QVBoxLayout(self)
        stack_layout.addWidget(text)
        stack_layout.addWidget(self.pix_graphics_view)

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
        self.people_detector.detect_and_bound_people(frame)

        image = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        if self.upscale:
            pixmap = QPixmap.fromImage(image).scaled(
                *UPSCALE_DIMENSIONS, Qt.KeepAspectRatio
            )
        else:
            pixmap = QPixmap.fromImage(image)
        # set the scene rect dynamically to fit the size of the pixmap, otherwise
        # the resulting view may not be centered correctly
        self.pix_graphics_view.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.pixmap_item.setPixmap(pixmap)

    def hide(self, **kwargs):
        """
        Hides the pixel view and stops the timer.

        :param kwargs: Additional keyword arguments to pass to the parent class's `hide` method.
        """
        super().hide(**kwargs)
        self.timer.stop()

    def show(self):
        """
        Displays the pixel view and starts the timer.
        """
        super().show()
        self.timer.start()

    def upscale_stream(self, is_upscaled: bool):
        """
        Sets whether the stream should be upscaled or not.

        Args:
            is_upscaled (bool): Whether the stream should be upscaled or not.
        """
        self.upscale = is_upscaled
