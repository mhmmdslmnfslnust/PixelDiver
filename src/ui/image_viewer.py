from io import BytesIO

from PIL.ImageQt import ImageQt

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel


class ImageViewer(QLabel):

    def __init__(self, placeholder=""):
        super().__init__()

        self.original_pixmap = None
        self.placeholder = placeholder

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumSize(400, 400)

        self.setText(self.placeholder)

        self.setStyleSheet("""
            QLabel{
                border:1px solid gray;
                background:white;
            }
        """)

    ####################################################

    def set_image(self, filename):

        self.original_pixmap = QPixmap(filename)
        self.update_view()

    ####################################################

    def set_pil_image(self, image):

        qt_image = ImageQt(image)

        self.original_pixmap = QPixmap.fromImage(qt_image)

        self.update_view()

    ####################################################

    def clear_image(self):

        self.original_pixmap = None

        self.setPixmap(QPixmap())

        self.setText(self.placeholder)

    ####################################################

    def update_view(self):

        if self.original_pixmap is None:
            return

        scaled = self.original_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.FastTransformation
        )

        self.setPixmap(scaled)

    ####################################################

    def resizeEvent(self, event):

        self.update_view()

        super().resizeEvent(event)