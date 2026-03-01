from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QLabel,QGridLayout
from PySide6.QtCore import Qt
import sys


class UniLog(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unilog")
        self.setGeometry(100, 100, 400, 300)
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


        self.ioLayout = QHBoxLayout() #Layer for the input and output of the conversion


        self.decimalInput = QLineEdit()
        self.decimalInput.setPlacehloderText("...")
        self.decimalInput.setStyleSheet("background-color: #34495e; color: white; border: none; padding: 5px;")
        self.ioLayout.addWidget(self.decimalInput)
        self.equals = QLabel(" = ")
        self.equals.setAlignment(Qt.AlignCenter)
        self.equals.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.ioLayout.addWidget(self.equals)
        self.binaryOutput = QGridLayout() # Binary output is not a single label, but a grid of small cells representing bits
        self.bitLabels = []
        




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UniLog()
    window.show()
    sys.exit(app.exec())