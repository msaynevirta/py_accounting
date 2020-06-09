from json import load, JSONDecodeError

def json_loader(filedir): # collect data from main json database
    try:
        with open(filedir,'r', encoding='utf-8') as data_file:
            data = load(data_file)
            return data

    except JSONDecodeError:
        print('\033[31m' + "Error: " + '\033[0m' + "Failed to read the data file")
        return False

class BlockAnalytics():
    """ Constructs two level tree hierarcy from totals collected from precollected data """
    def __init__(self, config_path, data_path, transaction_type, recipient_attribute_name, month):
        self.tree = []
        self.config = json_loader(config_path) # block config from config.csv
        self.raw_json_data = json_loader(data_path) # main json database

        self.transaction_type = transaction_type
        self.recipient_attribute_name = recipient_attribute_name
        self.month = str(month)

    def construct_tree(self, looped_var):
        """ Construct two level tree hierarcy from config """
        for level_1 in self.config:
            if level_1["sub"] is not None:
                sub_list = []
                for level_2 in level_1["sub"]:
                    sub_list.append([level_2["name"], self.collect_total_from_raw_data(level_2["path"]), None])
                
                self.tree.append([level_1["name"], sum(sub[1] for sub in sub_list), sub_list])
            
            else:
                self.tree.append([level_1["name"], self.collect_total_from_raw_data(level_1["path"]), None])

    def collect_total_from_raw_data(self, path):
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
            for it in self.raw_json_data[self.transaction_type]["months"][self.month]:
                try:
                    if(len(path) == 3 and
                       it["main_cat"] == main_cat and
                       it["sub_cat"] == sub_cat and
                       it[self.recipient_attribute_name] == beneficiary):
                        total += float(it["amount"])
                    elif(len(path) == 2 and
                         it["main_cat"] == main_cat and
                         it["sub_cat"] == sub_cat):
                        total += float(it["amount"])
                except KeyError:
                    print("Error reading values from transaction:", it[self.recipient_attribute_name],"on", it["entry_date"])
        except TypeError:
            total = 0.0
        
        return total

    def collect_savings(self, month):
        savings_in = 0.0
        savings_out = 0.0

        if month == 0: # collect all months
            for month in range(1,13):
                for it in self.config["savings"]["paths"]:
                    savings_out += self.collect_total_from_raw_data(["expenses", "beneficiary"])
                    savings_in += self.collect_total_from_raw_data(["income", "payer"])
        else: # collect single month
            for it in self.config["savings"]["paths"]:
                savings_out += self.collect_total_from_raw_data(["expenses", "beneficiary"])
                savings_in += self.collect_total_from_raw_data(["income", "payer"])

        return savings_in, savings_out

    def calculate_savings(self, month): 
        """ Calculate transactions between savings accounts """
        main_node = self.indexes.index(self.savings["main_node"])
        savings_node = self.indexes.index(self.savings["savings_node"])

        savings_in, savings_out = self.collect_savings(month)

        if savings_in > savings_out and self.transaction_type == "income":
            self.indexes.append("Säästötili")
            self.config.append([self.indexes.index("Säästötili"), (savings_in - savings_out), main_node])

        elif savings_in < savings_out and self.transaction_type == "expenses":
            self.indexes.append("Säästötili")
            self.config.append([savings_node, (savings_out - savings_in), self.indexes.index("Säästötili")])
            
            for it in self.config: # find savings node
                if it[2] == savings_node:
                    it[1] += (savings_out - savings_in) # add remaining savings to the savings node