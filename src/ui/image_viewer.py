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

    def set_image(self, filename):

        self.original_pixmap = QPixmap(filename)
        self.update_view()

    def update_view(self):

        if self.original_pixmap is None:
            self.setText(self.placeholder)
            return

        scaled = self.original_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

        self.setPixmap(scaled)

    def resizeEvent(self, event):

        self.update_view()

        super().resizeEvent(event)