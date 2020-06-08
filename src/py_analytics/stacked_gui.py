import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QStackedWidget, QHBoxLayout, QFileDialog, QPushButton
from PyQt5.QtCore import Qt

from transaction_loader import TransActionLoader

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.file_paths = []
        self.data = None

        self.setWindowTitle("Personal finances")

        self.home = QWidget()
        self.analytics = QWidget()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.home)
        self.stacked_widget.addWidget(self.analytics)

        self.stacked_widget.setCurrentIndex(0)

        self.setCentralWidget(self.stacked_widget)

        self.home_page()

    def home_page(self):
        button = QPushButton(self)
        button.setText("Choose transaction files")

        button.clicked.connect(self.loadTransactions)

        box = QHBoxLayout(self)
        box.setAlignment(Qt.AlignCenter)

        box.addWidget(button, alignment=Qt.AlignCenter)

        self.home.setLayout(box)

    def loadTransactions(self):
        self.file_paths, _ = QFileDialog.getOpenFileNames(self, "Choose transaction files", "/home", "JSON files (*.json)")
        self.data = TransActionLoader(self.file_paths).load_transactions()

    def analytics_page(self):
        pass

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()