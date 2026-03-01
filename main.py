from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QLabel,QGridLayout
from PySide6.QtCore import Qt
import sys


class UniLog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unilog")
        self.setGeometry(100, 100, 300, 300)
        self.setStyleSheet("background-color: #2c3e50; color: white; font-family: Arial;")
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)


        # First step: Create a way to convert decimal to binary and output it in a specified format

        self.firstLayout = QVBoxLayout() #Layer for the first step, including the title and the part for the conversion

        self.label1 = QLabel("Enter a decimal number to convert it to binary: It is CRUCIAL here")
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.firstLayout.addWidget(self.label1)
        self.mainLayout.addLayout(self.firstLayout)
        self.firstLayout.setAlignment(Qt.AlignTop)

        self.ioLayout = QHBoxLayout() #Layer for the input and output of the conversion

        self.ioLayout.setAlignment(Qt.AlignCenter)
        self.decimalInput = QLineEdit()
        self.decimalInput.setPlaceholderText("...")
        self.decimalInput.setStyleSheet("background-color: #34495e; color: white; border: none; padding: 7px; height: 10px;  ")
        self.ioLayout.addWidget(self.decimalInput)

        self.equals = QLabel(" = ")
        self.equals.setAlignment(Qt.AlignCenter)
        self.equals.setStyleSheet("font-size: 16px; font-weight: bold; ")
        self.ioLayout.addWidget(self.equals)
        self.binaryOutput = QGridLayout() # Binary output is not a single label, but a grid of small cells representing bits
        self.bitLabels = [] # ! bite equals 8 bits, so we will create 8 labels for the binary output
        for i in range(8):
            bitLabel = QLabel("0") # Initialize all bits to 0
            bitLabel.setAlignment(Qt.AlignCenter)
            bitLabel.setStyleSheet("background-color: #34495e; color: white; border: 1px solid #7f8c8d; padding: 7px; height : 10px; width: 10px;  ") # Style the bit labels to look like cells
            self.bitLabels.append(bitLabel)
            self.binaryOutput.addWidget(bitLabel, 0, i) # Add the bit label to the grid layout if the binary output has greater than 8 bits, we will need to add more rows to the grid layout
        self.ioLayout.addLayout(self.binaryOutput)

        self.convertButton = QPushButton("Convert")
        self.convertButton.setStyleSheet("background-color: #e74c3c; color: white; border: none; padding: 7px; font-size: 14px;")
        self.convertButton.setCursor(Qt.PointingHandCursor)
        self.convertButton.setFixedWidth(100)
        self.convertButton.setFixedHeight(30)
        self.convertButton.clicked.connect(self.convertDecimalToBinary)
        

        self.firstLayout.addLayout(self.ioLayout)
        self.firstLayout.addWidget(self.convertButton)

    def convertDecimalToBinary(self):
        decimalNumber = self.decimalInput.text()
        if decimalNumber.isdigit():
            decimalNumber = int(decimalNumber)
            binaryString = bin(decimalNumber)[2:]
            # Pad the binary string with leading zeros to ensure it is 8 bits long
            binaryString = binaryString.zfill(8)
            # Update the bit labels with the corresponding bits from the binary string
            print(binaryString)
            for i in range(8):
                self.bitLabels[i].setText(binaryString[i])
        else:
            # If the input is not a valid decimal number, reset the bit labels to 0
            for bitLabel in self.bitLabels:
                bitLabel.setText("0")

    



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UniLog()
    window.show()
    sys.exit(app.exec())