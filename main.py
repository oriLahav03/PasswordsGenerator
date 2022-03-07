from PyQt5 import QtWidgets
from gui import MainWindow

import sys


def main():
    app = QtWidgets.QApplication(sys.argv)
    my_mainWindow = QtWidgets.QMainWindow()
    ui = MainWindow(my_mainWindow)
    ui.setupUi()
    my_mainWindow.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
