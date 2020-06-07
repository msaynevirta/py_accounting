import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QWidget, QStackedWidget, QHBoxLayout, QFileDialog
from PyQt5.QtCore import Qt

# Subclass QMainWindow to customise your application's main window
class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("My Awesome App")

        self.page1 = SubWidget("test1")
        self.page2 = InitMessageBox()

        #self.page2.addLabel

        self.stackedWidget = QStackedWidget()

        self.stackedWidget.addWidget(self.page1)
        self.stackedWidget.addWidget(self.page2)

        self.stackedWidget.setCurrentIndex(1)

        self.setCentralWidget(self.stackedWidget)

class SubWidget(QWidget):
    def __init__(self, text, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        label = QLabel()
        layout = QHBoxLayout()

        label.setText(str(text))

        layout.addWidget(label)
        
        self.setLayout(layout)

class InitMessageBox(QWidget):
    def __init__(self, *args, **kwargs):
        super(QWidget, self).__init__(*args, **kwargs)
        self.msgbox = QFileDialog()

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()