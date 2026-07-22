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
    QDialog,
)

from ui.image_viewer import ImageViewer
from models.image_document import ImageDocument

from processing.processor import ImageProcessor
from processing.palette import PaletteManager
from export.image_exporter import ImageExporter
from ui.export_dialog import ExportDialog


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.document = ImageDocument()

        self.palette_manager = PaletteManager()     

        self.aspect_ratio = 1.0

        self.setWindowTitle("Diver")
        self.resize(1400, 750)

        self._create_menu()
        self._create_layout()

        self.load_palettes()

        self.statusBar().showMessage("Ready")

    ######################################################

    def _create_menu(self):

        file_menu = self.menuBar().addMenu("File")

        open_action = QAction("Open Image...", self)
        open_action.triggered.connect(self.open_image)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        export_action = QAction("Export Image...", self)
        export_action.triggered.connect(self.export_image)

        file_menu.addAction(open_action)
        file_menu.addAction(export_action)
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

        controls.addWidget(QLabel("Width"))

        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setRange(5, 300)
        self.width_slider.setValue(50)

        self.width_label = QLabel("50")

        controls.addWidget(self.width_slider)
        controls.addWidget(self.width_label)

        controls.addSpacing(15)

        controls.addWidget(QLabel("Height"))

        self.height_slider = QSlider(Qt.Horizontal)
        self.height_slider.setRange(5, 300)
        self.height_slider.setValue(50)

        self.height_label = QLabel("50")

        controls.addWidget(self.height_slider)
        controls.addWidget(self.height_label)

        controls.addSpacing(20)

        self.lock_ratio = QCheckBox("Lock Aspect Ratio")
        self.lock_ratio.setChecked(True)

        controls.addWidget(self.lock_ratio)

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

        self.palette_checkbox = QCheckBox(
            "Enable Palette Reduction"
        )

        controls.addWidget(self.palette_checkbox)

        self.palette_dropdown = QComboBox()

        controls.addWidget(self.palette_dropdown)

        ##################################################
        # Dithering
        ##################################################

        self.dithering_checkbox = QCheckBox(
            "Enable Floyd-Steinberg Dithering"
        )

        controls.addWidget(self.dithering_checkbox)

        ##################################################

        ##################################################
        # Grid
        ##################################################

        controls.addSpacing(20)

        controls.addWidget(QLabel("Grid"))

        self.grid_checkbox = QCheckBox("Show Grid")

        controls.addWidget(self.grid_checkbox)

        controls.addSpacing(10)

        controls.addWidget(QLabel("Cell Size"))

        self.cell_size_slider = QSlider(Qt.Horizontal)

        self.cell_size_slider.setRange(5, 40)
        self.cell_size_slider.setValue(20)

        controls.addWidget(self.cell_size_slider)

        self.cell_size_label = QLabel("20 px")

        controls.addWidget(self.cell_size_label)

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

        self.palette_dropdown.currentTextChanged.connect(
            self.update_preview
        )

        self.dithering_checkbox.stateChanged.connect(
            self.update_preview
        )

        self.grid_checkbox.stateChanged.connect(
            self.update_preview
        )

        self.cell_size_slider.valueChanged.connect(
            self.cell_size_changed
        )

    ######################################################
    def load_palettes(self):

        import os

        palette_folder = "palettes"

        if not os.path.isdir(palette_folder):
            return

        for filename in sorted(os.listdir(palette_folder)):

            if filename.endswith(".csv"):

                path = os.path.join(
                    palette_folder,
                    filename
                )

                self.palette_manager.load(path)

        self.palette_dropdown.clear()

        for name in self.palette_manager.names():

            self.palette_dropdown.addItem(name)

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
    
    def cell_size_changed(self, value):

        self.cell_size_label.setText(f"{value} px")

        self.update_preview()
    
    ######################################################
    
    def export_image(self):

        if self.document.processed is None:
            return

        dialog = ExportDialog(self)

        if dialog.exec() != QDialog.Accepted:
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Image",
            "output.png",
            "PNG Image (*.png);;JPEG Image (*.jpg)"
        )

        if not filename:
            return

        ImageExporter.save(
            self.document.processed,
            filename,
            scale=dialog.scale()
        )

        self.statusBar().showMessage(
            f"Exported: {filename}"
        )   
        
    ######################################################

    def update_preview(self):

        if self.document.original is None:
            return

        palette = None

        if (
            self.palette_checkbox.isChecked()
            and self.palette_dropdown.currentText()
        ):

            selected = self.palette_manager.get(
                self.palette_dropdown.currentText()
            )

            if selected is not None:
                palette = PaletteManager.rgb_list(selected)

        image = ImageProcessor.process(
            image=self.document.original,
            width=self.width_slider.value(),
            height=self.height_slider.value(),
            resize_method=self.resize_method.currentText(),
            palette=palette,
            dithering=self.dithering_checkbox.isChecked(),
            show_grid=self.grid_checkbox.isChecked(),
            cell_size=self.cell_size_slider.value(),
        )

        self.document.processed = image

        self.processed_label.set_pil_image(image)