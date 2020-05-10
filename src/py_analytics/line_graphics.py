from PyQt5.QtChart import QChart, QChartView

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

class LineDiagram():
    def __init__(self, qseries1, qseries2, legend, title):
        self.qseries1 = qseries1
        self.qseries2 = qseries2
        self.legend = legend
        self.title = title

    def create_linechart(self):
        chart = QChart()

        chart.addSeries(self.qseries1)
        chart.addSeries(self.qseries2)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(self.title)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        return chartview