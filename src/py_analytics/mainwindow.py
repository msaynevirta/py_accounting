import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtChart import QChart
from PyQt5.QtCore import Qt

from ui_mainwindow import Ui_MainWindow

from transaction_loader import TransActionLoader
from year_line_chart import YearLineAnalytics
from payment_methods import PaymentMethods

from quarterly_line_diagram import QuarterlyLineDiagram
from pie_graphics import PieDiagram

class MainWindow:
    def __init__(self):
        self.file_paths = []
        self.data = None

        self.main_window = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_window)
        self.ui.stackedWidget.setCurrentIndex(0) # Switch to home

        self.ui.btn_load.clicked.connect(self.load_transactions)

    def show(self):
        self.main_window.show()

    def load_transactions(self):
        self.file_paths, _ = QFileDialog.getOpenFileNames(self.ui.stackedWidget,
            "Choose transaction files", "/home", "JSON files (*.json)")
        self.data = TransActionLoader(self.file_paths).load_transactions()

        self.build_analytics()

    def build_analytics(self):
        self.cumulative_expenses_line()
        self.method_pie(max(self.data)) # Create chart for most recent year

        self.ui.stackedWidget.setCurrentIndex(1) # Switch to analytics

    def cumulative_expenses_line(self):
        two_largest_keys = [int(it) for it in sorted(self.data.keys(), reverse=True)[:2]]

        qlineseries_expenses = []

        for year in two_largest_keys:
            qlineseries_expenses.append(YearLineAnalytics(self.data, year))

        self.ui.v_cumulative_expenses.setChart(QuarterlyLineDiagram(qlineseries_expenses, "Cumulative expenses"))

    def method_pie(self, year):
        pie_chart = QChart()
        pie_chart.legend().hide()
        pie_chart.addSeries(PaymentMethods(self.data, year))
        pie_chart.createDefaultAxes()
        pie_chart.setAnimationOptions(QChart.SeriesAnimations)
        pie_chart.setTitle("Payment methods")

        pie_chart.legend().setVisible(True)
        pie_chart.legend().setAlignment(Qt.AlignBottom)

        self.ui.v_method_pie.setChart(pie_chart)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()

    # Start the Qt event loop. (i.e. make it possible to interact with the gui)
    sys.exit(app.exec_())