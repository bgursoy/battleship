import sys
from PyQt5.QtWidgets import QApplication
from window.setup_window import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Initialize setup window
    window = SetupWindow()
    window.show()
    # Run QT App
    app.exec_()
