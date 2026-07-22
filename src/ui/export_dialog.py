from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
)


class ExportDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle("Export")

        layout = QFormLayout(self)

        self.scale_combo = QComboBox()

        scales = [
            1,
            2,
            4,
            8,
            16,
            32,
            64
        ]

        for scale in scales:

            self.scale_combo.addItem(
                f"{scale}×",
                scale
            )

        self.scale_combo.setCurrentIndex(4)

        layout.addRow(
            "Scale:",
            self.scale_combo
        )

        buttons = QDialogButtonBox(

            QDialogButtonBox.Ok
            |
            QDialogButtonBox.Cancel

        )

        buttons.accepted.connect(self.accept)

        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

    ##################################################

    def scale(self):

        return self.scale_combo.currentData()