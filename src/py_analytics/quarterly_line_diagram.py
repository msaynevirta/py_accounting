from PyQt5.QtChart import QChart, QValueAxis, QCategoryAxis

from PyQt5.QtCore import Qt

class QuarterlyLineDiagram(QChart):
    """Builds a QChart line chart with transaction data from two latest years"""

    def __init__(self, qseries_list, title):
        super(QuarterlyLineDiagram, self).__init__()

        # Setup quarterly axis
        self.x_axis = QCategoryAxis()
        self.y_axis = QValueAxis()
        self.y_axis.setTickCount(6)

        self.x_axis.setMin(1)
        self.x_axis.setMax(366)

        self.x_axis.append("Q1", 91)
        self.x_axis.append("Q2", 182)
        self.x_axis.append("Q3", 274)
        self.x_axis.append("Q4", 365)


        # Setup chart
        self.setTitle(title)

        for series in qseries_list:
            self.addSeries(series)

        self.createDefaultAxes() # autoscale y-axis

        self.setAxisX(self.x_axis) # use predefined quarterly x-axis

        self.setAnimationOptions(QChart.SeriesAnimations)

        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)