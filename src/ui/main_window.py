from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QSlider,
    QComboBox,
    QCheckBox,
)

from ui.image_viewer import ImageViewer
from models.image_document import ImageDocument

from processing.processor import ImageProcessor
from processing.palette import Palettes


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.document = ImageDocument()

        self.aspect_ratio = 1.0

        self.setWindowTitle("Diver")
        self.resize(1400, 750)

        self._create_menu()
        self._create_layout()

        self.statusBar().showMessage("Ready")

    ######################################################

    def _create_menu(self):

        file_menu = self.menuBar().addMenu("File")

        open_action = QAction("Open Image...", self)
        open_action.triggered.connect(self.open_image)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

    ######################################################

    def _create_layout(self):

        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout()

        ##################################################
        # Sidebar
        ##################################################

        controls = QVBoxLayout()

        controls.addWidget(QLabel("<h2>Resize</h2>"))

        ##################################################

        controls.addWidget(QLabel("Width"))

        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setRange(5, 300)
        self.width_slider.setValue(50)

        self.width_label = QLabel("50")

        controls.addWidget(self.width_slider)
        controls.addWidget(self.width_label)

        ##################################################

        controls.addSpacing(15)

        controls.addWidget(QLabel("Height"))

        self.height_slider = QSlider(Qt.Horizontal)
        self.height_slider.setRange(5, 300)
        self.height_slider.setValue(50)

        self.height_label = QLabel("50")

        controls.addWidget(self.height_slider)
        controls.addWidget(self.height_label)

        ##################################################

        controls.addSpacing(20)

        self.lock_ratio = QCheckBox("Lock Aspect Ratio")
        self.lock_ratio.setChecked(True)

        controls.addWidget(self.lock_ratio)

        ##################################################

        controls.addSpacing(20)

        controls.addWidget(QLabel("Resize Method"))

        self.resize_method = QComboBox()

        self.resize_method.addItems([
            "Nearest",
            "Bilinear",
            "Bicubic",
            "Lanczos"
        ])

        controls.addWidget(self.resize_method)

        ##################################################
        # Palette
        ##################################################

        controls.addSpacing(20)

        self.palette_checkbox = QCheckBox("Enable Palette Reduction")

        controls.addWidget(self.palette_checkbox)

        ##################################################

        controls.addStretch()

        sidebar = QWidget()
        sidebar.setMaximumWidth(250)
        sidebar.setLayout(controls)

        ##################################################
        # Images
        ##################################################

        images = QHBoxLayout()

        self.original_label = ImageViewer("Original Image")
        self.processed_label = ImageViewer("Processed Preview")

        images.addWidget(self.original_label)
        images.addWidget(self.processed_label)

        ##################################################

        main_layout.addWidget(sidebar)
        main_layout.addLayout(images)

        central.setLayout(main_layout)

        ##################################################
        # Signals
        ##################################################

        self.width_slider.valueChanged.connect(self.width_changed)
        self.height_slider.valueChanged.connect(self.height_changed)

        self.resize_method.currentTextChanged.connect(
            self.update_preview
        )

        self.palette_checkbox.stateChanged.connect(
            self.update_preview
        )

    ######################################################

    def open_image(self):

        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.webp)"
        )

        if not filename:
            return

        self.document.load(filename)

        self.original_label.set_image(filename)

        width, height = self.document.original.size

        self.aspect_ratio = width / height

        self.width_slider.blockSignals(True)
        self.height_slider.blockSignals(True)

        self.width_slider.setValue(min(width, 300))
        self.height_slider.setValue(min(height, 300))

        self.width_slider.blockSignals(False)
        self.height_slider.blockSignals(False)

        self.width_label.setText(str(self.width_slider.value()))
        self.height_label.setText(str(self.height_slider.value()))

        self.update_preview()

        self.statusBar().showMessage(
            f"{filename} ({width} × {height})"
        )

    ######################################################

    def width_changed(self, value):

        self.width_label.setText(str(value))

        if self.lock_ratio.isChecked():

            h = round(value / self.aspect_ratio)

            self.height_slider.blockSignals(True)
            self.height_slider.setValue(max(5, min(h, 300)))
            self.height_slider.blockSignals(False)

            self.height_label.setText(
                str(self.height_slider.value())
            )

        self.update_preview()

    ######################################################

    def height_changed(self, value):

        self.height_label.setText(str(value))

        if self.lock_ratio.isChecked():

            w = round(value * self.aspect_ratio)

            self.width_slider.blockSignals(True)
            self.width_slider.setValue(max(5, min(w, 300)))
            self.width_slider.blockSignals(False)

            self.width_label.setText(
                str(self.width_slider.value())
            )

        self.update_preview()

    ######################################################

    def update_preview(self):

        if self.document.original is None:
            return

        palette = None

        if self.palette_checkbox.isChecked():
            palette = Palettes.BASIC

        image = ImageProcessor.process(
            image=self.document.original,
            width=self.width_slider.value(),
            height=self.height_slider.value(),
            resize_method=self.resize_method.currentText(),
            palette=palette,
            dithering=False,
        )

        self.document.processed = image

        self.processed_label.set_pil_image(image)