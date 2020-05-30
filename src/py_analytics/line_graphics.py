from PyQt5.QtChart import QChart, QChartView

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

class LineDiagram():
    def __init__(self, qseries_list, legend, title):
        self.qseries_list = qseries_list
        self.legend = legend
        self.title = title

    def create_linechart(self):
        chart = QChart()

        for series in self.qseries_list:
            chart.addSeries(series)

        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(self.title)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        return chartview