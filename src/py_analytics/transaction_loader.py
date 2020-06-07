from json import load, JSONDecodeError

class TransactionFileError(Exception):
    """Raise when reading json fails"""

class TransActionLoader():
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.data = {}

    def json_loader(self, filedir): # collect data from main json database
        try:
            with open(filedir,'r', encoding='utf-8') as data_file:
                return load(data_file)

        except JSONDecodeError:
            raise TransactionFileError("Failed to read a data file ({})".format(filedir))

    def load_transactions(self):
        for path in self.file_paths:
            try:
                transactions = self.json_loader(path)

                # Verify structure
                if transactions["year"] is not None and \
                    transactions["expenses"] is not None and \
                    transactions["income"] is not None:

                    self.data[str(transactions["year"])] = {
                        "expenses" : transactions["expenses"],
                        "income" : transactions["income"]
                    }

            except KeyError as err:
                print("Key error in file {}: {}".format(path, err))

            except TransactionFileError as err:
                print(err)

        return self.data

