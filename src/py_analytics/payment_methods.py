from json import load, JSONDecodeError

from PyQt5.QtChart import QPieSeries
from PyQt5.QtCore import pyqtSignal, QEvent

def json_loader(filedir): # collect data from main json database
    try:
        with open(filedir, 'r', encoding='utf-8') as data_file:
            data = load(data_file)
            return data

    except JSONDecodeError:
        print('\033[31m' + "Error: " + '\033[0m' + "Failed to read the data file")
        return False

class PaymentMethods(QPieSeries):
    '''
    Prepares pie chart of payment methods for plotting with PyQtCharts (supports currently only expenses)
    '''
    def __init__(self, data_path):
        super(PaymentMethods, self).__init__()
        self.raw_json_data = json_loader(data_path) # main json database
        
        series = {}

        for month in range(1,13):
            for transaction_type in ["expenses", "income"]: # go through both by month
                for it in self.raw_json_data[transaction_type]["months"][str(month)]:

                    main_key = it["payment_method"][0][0]
                    sub_key = it["payment_method"][0][1]

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



