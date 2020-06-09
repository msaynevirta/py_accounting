from json import load, JSONDecodeError

from PyQt5.QtChart import QPieSeries
from PyQt5.QtCore import pyqtSignal, QEvent

class PaymentMethods(QPieSeries):
    '''
    Prepares pie chart of payment methods for plotting with PyQtCharts (supports currently only expenses)
    '''
    def __init__(self, data, year):
        super(PaymentMethods, self).__init__()
        series = {}

        for month in range(1,13):
            for transaction_type in ["expenses", "income"]: # go through both by month
                for it in data[str(year)][transaction_type]["months"][str(month)]:
                    try:
                        main_key = it["payment_method"][0][0]
                        sub_key = it["payment_method"][0][1]
                    except IndexError:
                        continue

                    try:
                        series[main_key]
                    except KeyError:
                        series[main_key] = {}

                    try:
                        series[main_key][sub_key] += 1
                    except KeyError:
                        series[main_key][sub_key] = 1

        # convert dict to QPieSeries
        for main_key, sub_dicts in series.items():
            for sub_key in sub_dicts:
                self.append(''.join([main_key, sub_key]), sub_dicts[sub_key])



