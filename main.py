import sys
from PyQt5.QtWidgets import QApplication

from ui.window import SWBFWindow


def main():

    app = QApplication(sys.argv)

    w = SWBFWindow(810, 700)
    w.move(500, 50)
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
