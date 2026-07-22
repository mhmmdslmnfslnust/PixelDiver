from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QWidget,
)

from services.image_loader import ImageLoader


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.current_image = None

        self.setWindowTitle("Diver")
        self.resize(1200, 700)

        self._create_menu()
        self._create_layout()

        self.statusBar().showMessage("Ready")

    def _create_menu(self):

        file_menu = self.menuBar().addMenu("File")

        open_action = QAction("Open Image...", self)
        open_action.triggered.connect(self.open_image)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    def _create_layout(self):

        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout()

        self.original_label = QLabel("Original Image")
        self.processed_label = QLabel("Processed Preview\n\n(Coming in Phase 2)")

        for label in (self.original_label, self.processed_label):
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setMinimumSize(400, 400)
            label.setStyleSheet("""
                QLabel{
                    border:1px solid gray;
                    background:white;
                }
            """)

        layout.addWidget(self.original_label)
        layout.addWidget(self.processed_label)

        central.setLayout(layout)

    def open_image(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )

        if not filename:
            return

        self.current_image = ImageLoader.load(filename)

        pixmap = QPixmap(filename)

        self.original_label.setPixmap(
            pixmap.scaled(
                self.original_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        )

        self.statusBar().showMessage(filename)