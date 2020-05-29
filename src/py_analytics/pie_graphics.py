from PyQt5.QtChart import QChart, QChartView, QPieSlice

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen

class PieDiagram():
    def __init__(self, qseries, legend, title):
        self.qseries = qseries
        self.legend = legend
        self.title = title

    def create_piechart(self):
        #adding pie chart
        chart = QChart()
        chart.legend().hide()
        chart.addSeries(self.qseries)
        chart.createDefaultAxes()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTitle("Payment methods")

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)
 
        chartview = QChartView(chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        return chartview