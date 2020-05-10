from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QWidget, QHBoxLayout, QVBoxLayout

from year_line_chart import YearLineAnalytics
from line_graphics import LineDiagram

from block_graphics import BlockDiagram

class Window(QMainWindow):
    '''
    The class GUI handles the drawing of the main gui and allows user to
    interact with it.
    '''
    def __init__(self, expenses, income, level_amount):
        super(Window, self).__init__()
        self.setCentralWidget(QWidget())
        self.vertical = QVBoxLayout()
        self.horizontal = QHBoxLayout()
        self.centralWidget().setLayout(self.vertical)

        self.setWindowTitle("PyQtChart Line")
        self.setGeometry(100,100,1000,1000)
        #self.setCentralWidget(linediag)

        self.show()

        testdata = [
            {
                "dy": 433,
                "dx": 327.7153558052434,
                "x": 0,
                "y": 0
            },
            {
                "dy": 330.0862676056338,
                "dx": 372.2846441947566,
                "x": 327.7153558052434,
                "y": 0
            },
            {
                "dy": 102.9137323943662,
                "dx": 215.0977944236371,
                "x": 327.7153558052434,
                "y": 330.0862676056338
            },
            {
                "dy": 102.9137323943662,
                "dx": 68.94160077680677,
                "x": 542.8131502288805,
                "y": 330.0862676056338
            },
            {
                "dy": 80.40135343309854,
                "dx": 88.24524899431273,
                "x": 611.7547510056874,
                "y": 330.0862676056338
            },
            {
                "dy": 22.51237896126767,
                "dx": 88.2452489943124,
                "x": 611.7547510056874,
                "y": 410.4876210387323
            }
        ]

        # Add a view for showing the scene
        self.view = QGraphicsView(BlockDiagram(testdata, [], "Test").add_tree_items("income"), self)
        self.view.adjustSize()
        #self.view.show()
        self.vertical.addWidget(self.view)

        data_path = "/home/markus/repos/azure-accounting/src/data/main_database_2019.json"
        qseries_2019 = YearLineAnalytics(data_path).construct_cumulative_qseries(2019)

        data_path = "/home/markus/repos/azure-accounting/src/data/main_database.json"
        qseries_2020 = YearLineAnalytics(data_path).construct_cumulative_qseries(2019)

        self.linediag = LineDiagram(qseries_2019, qseries_2020, "empty", "Cumulative yearly expenses").create_linechart()
        self.linediag.setFixedSize(500,500)
        self.horizontal.addWidget(self.linediag)
        self.show()

        

        
