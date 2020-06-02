from PyQt5.QtChart import QChart, QChartView

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

class LineDiagram():
    def __init__(self, qseries_list, x_axis, title):
        self.qseries_list = qseries_list
        self.title = title
        self.x_axis = x_axis

    def create_linechart(self):
        chart = QChart()

        self.x_axis.setMin(0)
        self.x_axis.setMax(365)

        self.x_axis.append("Q1", 0)
        self.x_axis.append("Q2", 91)
        self.x_axis.append("Q3", 182)
        self.x_axis.append("Q4", 274)

        for series in self.qseries_list:
            #series.attachAxis(self.x_axis)
            chart.addSeries(series)
            chart.setAxisX(self.x_axis, series)

        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(self.title)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        return chartview