import sys
from PyQt5.QtWidgets import QApplication

from gui import Window

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