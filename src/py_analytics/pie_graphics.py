from PyQt5.QtChart import QChart, QChartView, QPieSlice

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen

class PieDiagram(QChart):
    def __init__(self, qseries, legend, title):
        super(PieDiagram, self).__init__()
        self.qseries = qseries
        self.legend = legend
        self.title = title

    def create_piechart(self):
        #adding pie chart
        self.legend().hide()
        self.addSeries(self.qseries)
        self.createDefaultAxes()
        self.setAnimationOptions(QChart.SeriesAnimations)
        self.setTitle("Payment methods")

        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)