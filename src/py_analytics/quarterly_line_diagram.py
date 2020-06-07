from PyQt5.QtChart import QChart, QChartView, QValueAxis, QLineSeries

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

class LineDiagram():
    def __init__(self, qseries_list, x_axis, title):
        self.qseries_list = qseries_list
        self.title = title

        self.x_axis = x_axis
        self.y_axis = QValueAxis()
        self.y_axis.setTickCount(6)

    def create_linechart(self):
        chart = QChart()

        self.x_axis.setMin(1)
        self.x_axis.setMax(366)

        self.x_axis.append("Q1", 91)
        self.x_axis.append("Q2", 182)
        self.x_axis.append("Q3", 274)
        self.x_axis.append("Q4", 365)

        series = QLineSeries()

        for series in self.qseries_list:
            chart.addSeries(series)

        chart.createDefaultAxes() # autoscale y-axis

        chart.setAxisX(self.x_axis) # use predefined quarterly x-axis

        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle(self.title)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        return chartview