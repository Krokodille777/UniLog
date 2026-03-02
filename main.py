from PySide6.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QLineEdit, QLabel, QGridLayout, QComboBox, QSpinBox
)
from PySide6.QtCore import Qt
import sys


class UniLog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unilog")
        self.setGeometry(100, 100, 600, 450)
        self.setStyleSheet(
            "background-color: #2c3e50; color: white; font-family: Arial;"
        )
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self._converted = False  # Track whether a conversion has been done

        # ── SECTION 1: Decimal → Binary Conversion ──────────────────────

        self.firstLayout = QVBoxLayout()
        self.firstLayout.setAlignment(Qt.AlignTop)

        self.label1 = QLabel("Enter a decimal number (0–255) to convert to binary:")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.firstLayout.addWidget(self.label1)

        # Input / output row
        self.ioLayout = QHBoxLayout()
        self.ioLayout.setAlignment(Qt.AlignCenter)

        self.decimalInput = QLineEdit()
        self.decimalInput.setPlaceholderText("e.g. 42")
        self.decimalInput.setStyleSheet(
            "background-color: #34495e; color: white; border: none; "
            "padding: 7px; height: 10px;"
        )
        self.ioLayout.addWidget(self.decimalInput)

        self.equals = QLabel(" = ")
        self.equals.setAlignment(Qt.AlignCenter)
        self.equals.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.ioLayout.addWidget(self.equals)

        # Binary bit grid (8 bits)
        self.binaryOutput = QGridLayout()
        self.bitLabels = []
        for i in range(8):
            bitLabel = QLabel("0")
            bitLabel.setAlignment(Qt.AlignCenter)
            bitLabel.setStyleSheet(
                "background-color: #34495e; color: white; "
                "border: 1px solid #7f8c8d; padding: 7px; "
                "height: 10px; width: 10px;"
            )
            self.bitLabels.append(bitLabel)
            self.binaryOutput.addWidget(bitLabel, 0, i)
        self.ioLayout.addLayout(self.binaryOutput)

        self.firstLayout.addLayout(self.ioLayout)

        # Error label for section 1
        self.errorLabel1 = QLabel("")
        self.errorLabel1.setAlignment(Qt.AlignCenter)
        self.errorLabel1.setStyleSheet("font-size: 12px; color: #e74c3c;")
        self.firstLayout.addWidget(self.errorLabel1)

        # Convert button
        self.convertButton = QPushButton("Convert")
        self.convertButton.setStyleSheet(
            "background-color: #e74c3c; color: white; border: none; "
            "padding: 7px; font-size: 14px;"
        )
        self.convertButton.setCursor(Qt.PointingHandCursor)
        self.convertButton.setFixedWidth(100)
        self.convertButton.setFixedHeight(30)
        self.convertButton.clicked.connect(self.convertDecimalToBinary)
        self.firstLayout.addWidget(self.convertButton, alignment=Qt.AlignCenter)

        self.mainLayout.addLayout(self.firstLayout)

        # Horizontal divider
        self.hr1 = QLabel()
        self.hr1.setFixedHeight(2)
        self.hr1.setStyleSheet("background-color: #7f8c8d;")
        self.mainLayout.addWidget(self.hr1)

        # ── SECTION 2: Bitwise Operations ────────────────────────────────

        self.secondLayout = QVBoxLayout()

        self.label2 = QLabel("Choose a bitwise operation:")
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.secondLayout.addWidget(self.label2)

        # Operation chooser row
        self.chooseOperationLayout = QHBoxLayout()

        self.operationComboBox = QComboBox()
        self.operationComboBox.setStyleSheet(
            "background-color: #34495e; color: white; border: none; "
            "padding: 7px; font-size: 14px;"
        )
        self.operationComboBox.addItems([
            "Invert String (NOT)",
            "Insert Bit (ADD | OR)",
            "Define Bit (AND)",
            "Clear Bit (AND (AND NOT))",
            "Invert Bit (XOR)",
        ])
        self.operationComboBox.currentTextChanged.connect(self._onOperationChanged)
        self.chooseOperationLayout.addWidget(self.operationComboBox)

        # Bit-position spinner (0–7) — much easier than typing a full mask
        self.bitPosLabel = QLabel("Bit position:")
        self.bitPosLabel.setStyleSheet("font-size: 13px;")
        self.chooseOperationLayout.addWidget(self.bitPosLabel)

        self.bitPosSpin = QSpinBox()
        self.bitPosSpin.setRange(0, 7)
        self.bitPosSpin.setValue(0)
        self.bitPosSpin.setStyleSheet(
            "background-color: #34495e; color: white; border: none; "
            "padding: 7px; font-size: 14px;"
        )
        self.bitPosSpin.setToolTip(
            "Bit 0 is the rightmost (least significant) bit, "
            "bit 7 is the leftmost (most significant) bit."
        )
        self.chooseOperationLayout.addWidget(self.bitPosSpin)

        # Show the generated mask so the student can see what's happening
        self.maskPreview = QLabel("Mask: 00000001")
        self.maskPreview.setStyleSheet("font-size: 12px; color: #95a5a6;")
        self.bitPosSpin.valueChanged.connect(self._updateMaskPreview)
        self.chooseOperationLayout.addWidget(self.maskPreview)

        self.secondLayout.addLayout(self.chooseOperationLayout)

        # Info label (shows which logical operation is being used)
        self.operationInfoLabel = QLabel("")
        self.operationInfoLabel.setAlignment(Qt.AlignCenter)
        self.operationInfoLabel.setStyleSheet("font-size: 12px; color: #95a5a6;")
        self.secondLayout.addWidget(self.operationInfoLabel)

        # Perform button
        self.performOperationButton = QPushButton("Perform Operation")
        self.performOperationButton.setStyleSheet(
            "background-color: #e74c3c; color: white; border: none; "
            "padding: 7px; font-size: 14px;"
        )
        self.performOperationButton.setCursor(Qt.PointingHandCursor)
        self.performOperationButton.clicked.connect(self.performOperation)

        self.clearBinaryResultButton = QPushButton("Clear Result")
        self.clearBinaryResultButton.setStyleSheet("background-color: #7f8c8d; color: white; border: none; "
        "padding: 7px; font-size: 14px;")
        self.clearBinaryResultButton.setCursor(Qt.PointingHandCursor)
        self.clearBinaryResultButton.clicked.connect(self.clearBinaryResult)


        #Special layout for perform and clear buttons to be side by side
        self.buttonsLayout = QHBoxLayout()
        self.buttonsLayout.addWidget(self.performOperationButton, alignment=Qt.AlignCenter)
        self.buttonsLayout.addWidget(self.clearBinaryResultButton, alignment=Qt.AlignCenter)
        self.secondLayout.addLayout(self.buttonsLayout)

        # ── Result row: decimal = binary grid ────────────────────────────

        self.resultRow = QHBoxLayout()
        self.resultRow.setAlignment(Qt.AlignCenter)

        self.decimalResultLabel = QLabel("Result: –")
        self.decimalResultLabel.setAlignment(Qt.AlignCenter)
        self.decimalResultLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.resultRow.addWidget(self.decimalResultLabel)

        self.equals2 = QLabel(" = ")
        self.equals2.setAlignment(Qt.AlignCenter)
        self.equals2.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.resultRow.addWidget(self.equals2)

        self.binaryOutput2 = QGridLayout()
        self.resultBitLabels = []
        for i in range(8):
            lbl = QLabel("0")
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet(
                "background-color: #34495e; color: white; "
                "border: 1px solid #7f8c8d; padding: 7px; "
                "height: 10px; width: 10px;"
            )
            self.resultBitLabels.append(lbl)
            self.binaryOutput2.addWidget(lbl, 0, i)
        self.resultRow.addLayout(self.binaryOutput2)

        self.secondLayout.addLayout(self.resultRow)
        self.mainLayout.addLayout(self.secondLayout)

        # ── Collect all section-2 widgets so we can enable/disable them ──
        self._section2Widgets = [
            self.operationComboBox,
            self.bitPosSpin,
            self.performOperationButton,
            self.clearBinaryResultButton,
        ]

        # Initial state: hide bit-position for NOT, disable section 2
        self._onOperationChanged(self.operationComboBox.currentText())
        self._setSection2Enabled(False)

    # ── Helpers ──────────────────────────────────────────────────────────

    def _setSection2Enabled(self, enabled: bool):
        """Enable or disable all interactive widgets in the operations section."""
        for w in self._section2Widgets:
            w.setEnabled(enabled)

    def _onOperationChanged(self, text: str):
        """Show/hide the bit-position input depending on the operation."""
        is_not = text.startswith("Invert String")
        self.bitPosLabel.setVisible(not is_not)
        self.bitPosSpin.setVisible(not is_not)
        self.maskPreview.setVisible(not is_not)

    def _updateMaskPreview(self):
        pos = self.bitPosSpin.value()
        mask = self._makeMask(pos)
        self.maskPreview.setText(f"Mask: {mask}")

    @staticmethod
    def _makeMask(position: int) -> str:
        """Return an 8-bit string with only the given bit set (bit 0 = rightmost)."""
        value = 1 << position
        return bin(value)[2:].zfill(8)

    # ── Conversion ───────────────────────────────────────────────────────

    def convertDecimalToBinary(self):
        self.errorLabel1.setText("")
        text = self.decimalInput.text().strip()

        if not text.isdigit():
            self.errorLabel1.setText("Please enter a valid non-negative integer.")
            self._resetBits(self.bitLabels)
            self._setSection2Enabled(False)
            return

        value = int(text)
        if value > 255:
            self.errorLabel1.setText(
                "Value exceeds 255 (max for 8 bits). Please enter 0–255."
            )
            self._resetBits(self.bitLabels)
            self._setSection2Enabled(False)
            return

        binary = bin(value)[2:].zfill(8)
        for i in range(8):
            self.bitLabels[i].setText(binary[i])

        # Unlock the operations section
        self._converted = True
        self._setSection2Enabled(True)

    @staticmethod
    def _resetBits(labels):
        for lbl in labels:
            lbl.setText("0")

    # ── Bitwise engine ───────────────────────────────────────────────────

    @staticmethod
    def convertBinaryToDecimal(binaryString: str) -> int:
        return int(binaryString, 2)

    @staticmethod
    def performNOT(bits: str) -> str:
        return "".join("1" if b == "0" else "0" for b in bits)

    @staticmethod
    def performAND(a: str, b: str) -> str:
        return "".join("1" if x == "1" and y == "1" else "0" for x, y in zip(a, b))

    @staticmethod
    def performOR(a: str, b: str) -> str:
        """Binary addition with carry, clamped to 8 bits (max 255)."""
        result = int(a, 2) + int(b, 2)
        if result > 255:
            result = 255  # clamp to 8-bit max
        return ''.join (bin(result)[2:].zfill(8))

    @staticmethod
    def performANDNOT(a: str, b: str) -> str:
        """Perform a AND NOT b (a AND (NOT b))."""
        #Inverted mask means we want to keep all bits of a except the one we're clearing
        inverted_b = UniLog.performNOT(b)
        return UniLog.performAND(a, inverted_b)

    @staticmethod
    def performXOR(a: str, b: str) -> str:
        return "".join(
            "1" if (x == "1") ^ (y == "1") else "0" for x, y in zip(a, b)
        )

    # ── Perform the chosen operation ─────────────────────────────────────

    def performOperation(self):
        operation = self.operationComboBox.currentText()
        binaryString1 = "".join(lbl.text() for lbl in self.bitLabels)
        mask = self._makeMask(self.bitPosSpin.value())

        if operation == "Invert String (NOT)":
            self.operationInfoLabel.setText(f"NOT {binaryString1}")
            result = self.performNOT(binaryString1)

        elif operation == "Insert Bit (ADD | OR)":
            self.operationInfoLabel.setText(
                f"{binaryString1} OR {mask}"
            )
            result = self.performOR(binaryString1, mask)

        elif operation == "Define Bit (AND)":
            self.operationInfoLabel.setText(
                f"{binaryString1} AND {mask}"
            )
            result = self.performAND(binaryString1, mask)

        elif operation == "Clear Bit (AND (AND NOT))":
            self.operationInfoLabel.setText(
                f"{binaryString1} AND NOT {mask}"
            )
            result = self.performANDNOT(binaryString1, mask)

        elif operation == "Invert Bit (XOR)":
            self.operationInfoLabel.setText(
                f"{binaryString1} XOR {mask}"
            )
            result = self.performXOR(binaryString1, mask)
        else:
            return
        
       

        # Update result grid
        for i in range(8):
            self.resultBitLabels[i].setText(result[i])

        # Update decimal result label
        decimal = self.convertBinaryToDecimal(result)
        self.decimalResultLabel.setText(f"Result: {decimal}")

    def clearBinaryResult(self):
         #Clear button sets result bits to 0 and decimal result to –
        for lbl in self.resultBitLabels:
            lbl.setText("0")
        self.decimalResultLabel.setText("Result: –")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UniLog()
    window.show()
    sys.exit(app.exec())