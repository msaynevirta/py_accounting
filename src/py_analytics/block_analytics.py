import csv
from json import load, JSONDecoder, JSONDecodeError

def json_loader(filedir): # collect data from main json database
    try:
        with open(filedir,'r', encoding='utf-8') as data_file:
            data = load(data_file)
            return data

    except JSONDecodeError:
        print('\033[31m' + "Error: " + '\033[0m' + "Failed to read the data file")
        return False

class BlockAnalytics:
    def __init__(self, config_path, data_path):
        self.config = []
        self.indexes = []
        self.savings = []
        self.raw_json_config = json_loader(config_path) # block config from config.csv
        self.raw_json_data = json_loader(data_path) # main json database

    def collect_total_from_raw_data(self, transaction_type, recipient, path, month):
        main_cat = False
        sub_cat = False
        beneficiary = False
        total = 0.0

        if(len(path) == 2):
            main_cat = path[0]
            sub_cat = path[1]

        elif(len(path) == 3):
            main_cat = path[0]
            sub_cat = path[1]
            beneficiary = path[2]

        try:
            for it in self.raw_json_data[transaction_type]["months"][str(month)]:
                try:
                    if(len(path) == 3 and
                    it["main_cat"] == main_cat and
                    it["sub_cat"] == sub_cat and
                    it[recipient] == beneficiary):
                            total += float(it["amount"])
                            
                    elif(len(path) == 2 and
                        it["main_cat"] == main_cat and
                        it["sub_cat"] == sub_cat):
                            total += float(it["amount"])
                except KeyError:
                    print("Error reading values from transaction:", it[recipient],"on", it["entry_date"])
        except TypeError:
            total = 0.0
        
        return total

    def collect_total_from_existing(self, mode, src, dest):
        total = 0.0

        if(mode == 0): # collect values from src
            for it in self.config:
                if it[2] == src:
                    total += it[1]

        elif(mode == 1): # collect values from dest
            for it in self.config:
                if it[0] == dest:
                    total += it[1]

        return total

    def load_config(self):
        for it in self.raw_json_config["links"]:
            # save human readable names to a index db
            if(not it["source"]["name"] in self.indexes):
                self.indexes.append(it["source"]["name"])

            if(not it["destination"]["name"] in self.indexes):
                self.indexes.append(it["destination"]["name"])

            src = self.indexes.index(it["source"]["name"])
            dest = self.indexes.index(it["destination"]["name"])

            link_list = [src, 0.0, dest]

            # convert names to machine readable indexes & create list of links
            self.config.append(link_list)
        
        # list of savings accounts
        self.savings = self.raw_json_config["savings"]

    def populate_config(self, month):
        for it in self.config:
            src = self.indexes[it[0]]
            dest = self.indexes[it[2]]

            for it_raw_data in self.raw_json_config["links"]:
                if(it_raw_data["source"]["name"] == src and it_raw_data["destination"]["name"] == dest):
                    if(isinstance(it_raw_data["source"]["path"], list)): # determine from src side (income)
                        it[1] += self.collect_total_from_raw_data("income", "payer", it_raw_data["source"]["path"], month)

                    elif(isinstance(it_raw_data["destination"]["path"], list)): # determine from dest side (expenses)
                        it[1] += self.collect_total_from_raw_data("expenses", "beneficiary", it_raw_data["destination"]["path"], month)

                    else: # determine from other links
                        if(it_raw_data["source"]["path"] != None):
                            it[1] = self.collect_total_from_existing(0, it[0], it[2])
                        
                        elif(it_raw_data["destination"]["path"] != None):
                            it[1] = self.collect_total_from_existing(1, it[0], it[2])
            
            print(it)

    def collect_savings(self, month):
        savings_in = 0.0
        savings_out = 0.0

        if month == 0: # collect all months
            for month in range(1,13):
                for it in self.savings["paths"]:
                    savings_out += self.collect_total_from_raw_data("expenses", "beneficiary", it, month)
                    savings_in += self.collect_total_from_raw_data("income", "payer", it, month)
        else: # collect single month
            for it in self.savings["paths"]:
                savings_out += self.collect_total_from_raw_data("expenses", "beneficiary", it, month)
                savings_in += self.collect_total_from_raw_data("income", "payer", it, month)

        return savings_in, savings_out

    def calculate_savings(self, month): # calculate transactions between savings accounts
        main_node = self.indexes.index(self.savings["main_node"])
        savings_node = self.indexes.index(self.savings["savings_node"])

        savings_in, savings_out = self.collect_savings(month)

        if(savings_in > savings_out):
            self.indexes.append("Säästötili")
            self.config.append([self.indexes.index("Säästötili"), (savings_in - savings_out), main_node])

        elif(savings_in < savings_out):
            self.indexes.append("Säästötili")
            self.config.append([savings_node, (savings_out - savings_in), self.indexes.index("Säästötili")])
            
            for it in self.config: # find savings node
                if it[2] == savings_node:
                    it[1] += (savings_out - savings_in) # add remaining savings to the savings node
