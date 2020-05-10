import sys
from PyQt5.QtWidgets import QApplication, QGraphicsRectItem

from block_analytics import BlockAnalytics
from gui import Window

class BlockGraphicsItem(QGraphicsRectItem):
    '''
    Handles drawing of blocks
    '''

class BlockDiagram(BlockGraphicsItem):
    def __init__(self, expenses, income):
        super(BlockDiagram, self).__init__()

    def load_level(self, type, depth):
        pass # loads data from certain level in income/expenses

    def load_data(self):
        # init with January
        it = BlockAnalytics(
            "/home/markus/repos/azure-accounting/src/data/sankey_config.json",
            "/home/markus/repos/azure-accounting/src/data/main_database.json")
        it.load_config()

        for month in range(1, 13):
            print("month: {:d}\n".format(month))
            it.populate_config(month)

        it.calculate_savings(0)

def main():
    # Every Qt application must have one instance of QApplication.
    global APP # Use global to prevent crashing on exit
    APP = QApplication(sys.argv)
    window = Window(0,0,0)

    window.show()

    # Start the Qt event loop. (i.e. make it possible to interact with the gui)
    sys.exit(APP.exec_())

    # Any code below this point will only be executed after the gui is closed.

if __name__ == '__main__':
    main()