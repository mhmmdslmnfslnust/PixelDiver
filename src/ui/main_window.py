from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from ui.image_viewer import ImageViewer
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

        self.original_label = ImageViewer("Original Image")

        self.processed_label = ImageViewer(
            "Processed Preview\n\n(Coming in Phase 3)"
        )

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

        self.original_label.set_image(filename)

        self.statusBar().showMessage(filename)