from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QMainWindow, QAction, QTabWidget, QWidget, QGridLayout, QStyle, QFileDialog, QPushButton, \
    QLineEdit, QHBoxLayout, QToolButton

from runner import Runner
from ui.tab import ServerTab

STEAM_PATH = 'C:/Program Files (x86)/Steam/steamapps/common/Star Wars Battlefront (Classic 2004)/GameData/Battlefront.exe'
GOG_PATH = 'C:/Program Files (x86)/GOG Galaxy/Games/Star Wars - Battlefront/GameData/Battlefront.exe'


class SWBFWindow(QMainWindow):
    def __init__(self, w, h):
        super().__init__()

        self._runner = Runner()

        self.setFixedSize(w, h)
        self.setWindowTitle('SWBF Server')

        # Layout
        self._main_widget = QWidget()
        self._main_grid = QGridLayout(self._main_widget)
        self.setCentralWidget(self._main_widget)

        # Statusbar
        self.statusBar().showMessage('Ready')

        # Menubar
        file_menu = self.menuBar().addMenu('&File')
        file_menu.addAction(QAction('&Open', self))
        file_menu.addAction(QAction('&Exit', self))

        # Toolbar
        toolbar = self.addToolBar('Run')

        self.run = QToolButton()
        self.run.setDefaultAction(QAction(self.style().standardIcon(QStyle.SP_MediaPlay), '&Run', self))
        self.run.setDisabled(True)

        self.stop = QToolButton()
        self.stop.setDefaultAction(QAction(self.style().standardIcon(QStyle.SP_MediaStop), '&Stop', self))
        self.stop.setDisabled(True)

        toolbar.addWidget(self.run)
        toolbar.addWidget(self.stop)

        # Executable selection
        self._file_select_wrapper = QWidget()
        self._file_select = QHBoxLayout(self._file_select_wrapper)
        self._file_select_button = QPushButton('Select Executable')
        self._file_select_value = QLineEdit('')
        self._file_select.addWidget(self._file_select_button)
        self._file_select.addWidget(self._file_select_value)

        if QFileInfo(STEAM_PATH).exists():
            self._file_select_value.setText(STEAM_PATH)
        # elif QFileInfo(GOG_PATH).exists():
        #     self._file_select_value.setText(GOG_PATH)

        # Tab widget
        self._tabs = QTabWidget()
        self._tabs.addTab(ServerTab('Server 1', self._tabs, 0), 'Server 1')

        #self.add_tab = QWidget()
        # self.tabs.addTab(self.add_tab, '+')
        # self.tabs.currentChanged.connect(self._tab_changed)

        self._main_grid.addWidget(self._file_select_wrapper)
        self._main_grid.addWidget(self._tabs)

        # Events
        self._file_select_button.clicked.connect(self._open_file_dialog)
        self._file_select_value.textChanged.connect(self._check_exe)
        self.run.clicked.connect(self._start_server)
        self.stop.clicked.connect(self._stop_server)

        # Init
        self._check_exe()

    def _check_exe(self):
        if self._file_select_value.text():
            self.run.setDisabled(False)

    def _start_server(self):
        self._runner.add_process(self._file_select_value.text(), self._tabs.currentWidget().options())
        self.run.setDisabled(True)
        self.stop.setDisabled(False)

    def _stop_server(self):
        self._runner.stop_process()
        self.run.setDisabled(False)
        self.stop.setDisabled(True)

    def _open_file_dialog(self):
        dialog = QFileDialog(filter='*.exe')
        if dialog.exec_():
            self._file_select_value.setText(dialog.selectedFiles()[0])

    def _tab_changed(self, index):
        if index == self._tabs.count() - 1:
            new_index = self._tabs.count()
            tab_name = 'Server ' + str(new_index)
            new_tab = ServerTab(tab_name, self._tabs, new_index + 1)
            self._tabs.addTab(new_tab, tab_name)
            self._tabs.setTabOrder(new_tab, self.add_tab)
