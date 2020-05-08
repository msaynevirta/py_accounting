from PyQt5.QtWidgets import QMainWindow

from py_gui.py_analytics.year_line_chart import YearLineAnalytics
from py_gui.line_graphics import LineDiagram

class Window(QMainWindow):
    '''
    The class GUI handles the drawing of the main gui and allows user to
    interact with it.
    '''
    def __init__(self, expenses, income, level_amount):
        super(Window, self).__init__()
        
        date_path = "/home/markus/repos/azure-accounting/src/data/main_database_2019.json"
        qseries = YearLineAnalytics(date_path).construct_cumulative_qseries(2019)

        linediag = LineDiagram(qseries, "empty", "Cumulative yearly expenses").create_linechart()

        self.setWindowTitle("PyQtChart Line")
        self.setGeometry(100,100, 680,500)
        self.setCentralWidget(linediag)

        self.show()
