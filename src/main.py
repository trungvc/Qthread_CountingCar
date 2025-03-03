from PyQt5.QtWidgets import QApplication
from main_window import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    app.aboutToQuit.connect(main_win.close)
    sys.exit(app.exec())
