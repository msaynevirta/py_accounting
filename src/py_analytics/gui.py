from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QWidget, QHBoxLayout, QVBoxLayout

from year_line_chart import YearLineAnalytics
from line_graphics import LineDiagram

from pie_graphics import PieDiagram
from payment_methods import PaymentMethods

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

        data_list = [["/home/markus/repos/azure-accounting/src/data/main_database_2019.json", 2019], ["/home/markus/repos/azure-accounting/src/data/main_database.json", 2020]]
        data_path = "/home/markus/repos/azure-accounting/src/data/main_database.json"

        self.draw_method_pie(data_path)
        self.draw_cumulative_line(data_list)
        self.linediag.setFixedSize(500,500)

        self.horizontal.addWidget(self.linediag)
        self.horizontal.addWidget(self.piediag)

        self.vertical.addLayout(self.horizontal)

        self.show()

    def draw_method_pie(self, data_path):
        pie_qseries_2020 = PaymentMethods(data_path)
        self.piediag = PieDiagram(pie_qseries_2020, "empty", "Cumulative yearly expenses").create_piechart()

    def draw_cumulative_line(self, data_list):
        line_qseries_list = []

        for row in data_list:
            line_qseries_list.append(YearLineAnalytics(row[0]).construct_cumulative_qseries(row[1]))

        self.linediag = LineDiagram(line_qseries_list, "empty", "Cumulative yearly expenses").create_linechart()
        

        
