from json import load, JSONDecodeError
from datetime import datetime, timedelta
from calendar import isleap

from PyQt5.QtChart import QLineSeries

def json_loader(filedir): # collect data from main json database
    try:
        with open(filedir,'r', encoding='utf-8') as data_file:
            data = load(data_file)
            return data

    except JSONDecodeError:
        print('\033[31m' + "Error: " + '\033[0m' + "Failed to read the data file")
        return False

class YearLineAnalytics:
    def __init__(self, data_path):
        self.raw_json_data = json_loader(data_path) # main json database

    def collect_total_from_raw_data(self, transaction_type, recipient_type, month, date_nr):
        '''
        Collects daily totals from raw data, doesn't take savings currently into account
        '''
        total = 0.0
        try:
            for it in self.raw_json_data[transaction_type]["months"][str(month)]:
                try:
                    if date_nr == datetime.strptime(it["entry_date"], "%Y-%m-%dT%H:%M:%S%z").timetuple().tm_yday:
                        total += float(it["amount"])

                except KeyError:
                    print("Error reading values from transaction:", it[recipient_type],"on", it["entry_date"])

                except ValueError as err:
                    print(err)
        except TypeError:
            total = 0.0
        
        return total

    def construct_cumulative_qseries(self, year):
        '''
        Prepares cumulative data time series for plotting with PyQtCharts (supports currently only expenses)
        '''
        days_in_year = 365

        qseries = QLineSeries()
        if isleap(year):
            days_in_year = 366

        for day in range(1, days_in_year+1):
            month = (datetime(year, 1, 1) + timedelta(day - 1)).timetuple().tm_mon
            
            cumulative_total = float(qseries.at(day-2).y()) + self.collect_total_from_raw_data("expenses", "beneficiary", month, day)
            qseries.append(day, cumulative_total)

        return qseries



