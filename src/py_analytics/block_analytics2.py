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
    def __init__(self, config_path, data_path, transaction_type, recipient_attribute_name, month):
        self.links = []
        self.config = json_loader(config_path) # block config from config.csv
        self.raw_json_data = json_loader(data_path) # main json database

        self.transaction_type = transaction_type
        self.recipient_attribute_name = recipient_attribute_name
        self.month = str(month)

    def loop_links(self, looped_var):
        name = None
        sub_list = []
        total = 0

        for it in looped_var:
            if it["sub"] is not None:
                sub = self.loop_links(it["sub"])[2]
                sub_list = sub[2]
                total += sub[1]

            else:
                # append to links!!!
                name = it["name"]
                total += self.collect_total_from_raw_data(it["path"])

        return list(name, total, sub_list)


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

    def populate_config(self):
        self.loop_links(self.config)