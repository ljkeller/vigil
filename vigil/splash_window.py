"""Implements the Vigil splash screen widget (precursor to the main window).)"""

import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QSplashScreen

from vigil.generated_ui.splash_ui import SplashUI

class VigilSplashWindow(QSplashScreen):
    """A custom splash screen widget with a progress bar for the Vigil application."""

    def __init__(self):
        super(QSplashScreen, self).__init__()

        self.ui = SplashUI()
        self.ui.setupUi(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        pixmap = QPixmap("images/splash_grad.png")
        self.setPixmap(pixmap)

        self.center()

    def progress(self):
        """
        Iteratively updates the progress bar on the user interface.
        """
        for i in range(101):
            time.sleep(0.01)
            self.ui.progress_bar.setValue(i)
            QApplication.processEvents()

    def center(self):
        """
        Centers the splash screen on the user's screen.
        """
        relative_geometry = self.frameGeometry()
        center_point = QApplication.desktop().availableGeometry().center()
        relative_geometry.moveCenter(center_point)
        self.move(relative_geometry.topLeft())
