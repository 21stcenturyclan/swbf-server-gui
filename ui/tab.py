from PyQt5 import QtCore
from PyQt5.QtWidgets import QLineEdit, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPlainTextEdit, QTreeWidget, \
    QTreeWidgetItem, QScrollArea

from ui.widgets import PairWidget, MapSelection, Separator, CheckboxPairWidget, SliderPairWidget, LineEditPairWidget

MAP_NAMES = [
    'Bespin: Cloud City',
    'Bespin: Platforms',
    'Endor: Bunker',
    'Geonosis: Spire',
    'Hoth: Echo Basis',
    'Kamino: Tipoca City',
    'Kashyyyk: Island',
    'Kashyyyk: Docks',
    'Naboo: Plains',
    'Naboo: Theed',
    'Rhen Var: Citadell',
    'Rhen Var: Harbor',
    'Tatooine: Dune Sea',
    'Tatooine: Jabba\'s Palace',
    'Tatooine: Mos Eisley',
    'Yavin IV: Arena',
    'Yavin IV: Temple']

MAP_ID = {
    'Bespin: Cloud City':        {'CW': 'bes2r', 'GCW': 'bes2a'},
    'Bespin: Platforms':         {'CW': 'bes1r', 'GCW': 'bes1a'},
    'Endor: Bunker':             {'GCW': 'end1a'},
    'Geonosis: Spire':           {'CW': 'geo1r'},
    'Hoth: Echo Basis':          {'GCW': 'hot1i'},
    'Kamino: Tipoca City':       {'CW': 'kam1c'},
    'Kashyyyk: Docks':           {'CW': 'kas2c', 'GCW': 'kas2i'},
    'Kashyyyk: Island':          {'CW': 'kas1c', 'GCW': 'kas1i'},
    'Naboo: Plains':             {'CW': 'nab1c', 'GCW': 'nab1i'},
    'Naboo: Theed':              {'CW': 'nab2c', 'GCW': 'nab2a'},
    'Rhen Var: Citadell':        {'CW': 'rhn2c', 'GCW': 'rhn2a'},
    'Rhen Var: Harbor':          {'CW': 'rhn1r', 'GCW': 'rhn1i'},
    'Tatooine: Dune Sea':        {'CW': 'tat1r', 'GCW': 'tat1i'},
    'Tatooine: Jabba\'s Palace': {'CW': 'tat3c', 'GCW': 'tat3a'},
    'Tatooine: Mos Eisley':      {'CW': 'tat2r', 'GCW': 'tat2i'},
    'Yavin IV: Arena':           {'CW': 'yav2r', 'GCW': 'yav2i'},
    'Yavin IV: Temple':          {'CW': 'yav1c', 'GCW': 'yav1i'}
}


class ServerTab(QWidget):
    def __init__(self, name, parent, id):
        super().__init__()

        self._tab_parent = parent
        self._tab_id = id
        self._init = False

        self._create(name)
        self._init = True
        self._map_widget.add(0)
        self._new_map(MAP_NAMES[0])
        self._update_options()

    def _create(self, name):
        self._hbox = QHBoxLayout(self)

        self._left_scroll = QWidget()
        self._scroll = QScrollArea()

        self._left_wrapper = QWidget()
        self._left_wrapper.setMaximumWidth(self.width() * 0.66)
        self._left = QVBoxLayout(self._left_wrapper)
        self._left.setContentsMargins(0, 0, 0, 0)
        self._left.setSpacing(0)

        self._right_wrapper = QWidget()
        self._right_wrapper.setMaximumWidth(self.width() * 0.5)
        self._right = QVBoxLayout(self._right_wrapper)

        self._create_left_column(name)
        self._create_right_column()

        self._scroll.setWidget(self._left_wrapper)
        self._hbox.addWidget(self._scroll)
        self._hbox.addWidget(self._right_wrapper)

    def _create_left_column(self, name):
        self._server_name = LineEditPairWidget('Servername:', name).on_change(self._update_options)
        self._server_password = LineEditPairWidget('Password:', '').on_change(self._update_options)
        self._server_admin_pw = LineEditPairWidget('Admin password:', '').on_change(self._update_options)

        self._server_type = CheckboxPairWidget('Dedicated:').on_change(self._update_options)
        self._windowed = CheckboxPairWidget('Windowed:').on_change(self._update_options)
        self._resolution = PairWidget(QLabel('Resolution:'), PairWidget(QLineEdit('200'), QLineEdit('200')))
        self._lan = CheckboxPairWidget('Lan:').on_change(self._update_options)
        self._ticks_per_second = SliderPairWidget('TPS:', 30, 60, 60).on_change(self._update_options)
        self._throttle = SliderPairWidget('Bandwidth per Client:', 1000, 10000, 6000).on_change(self._update_options)
        self._spawn = SliderPairWidget('Spawn:', 0, 10, 2).on_change(self._update_options)
        self._log = CheckboxPairWidget('Log:').on_change(self._update_options)

        self._player_limit = SliderPairWidget('Player limit:', 1, 32, 20).on_change(self._update_options)
        self._player_count = SliderPairWidget('Player count:', 1, 32, 2).on_change(self._update_options)
        self._player_select = CheckboxPairWidget('Player select:', True).on_change(self._update_options)
        self._show_names = CheckboxPairWidget('Player names:', True).on_change(self._update_options)
        self._number_of_bots = SliderPairWidget('Bots:', 0, 32, 0).on_change(self._update_options)
        self._bot_difficulty = SliderPairWidget('AI Difficulty:', 1, 3, 2).on_change(self._update_options)
        self._team_damage = CheckboxPairWidget('Team damage:', True).on_change(self._update_options)
        self._heroes = CheckboxPairWidget('Heroes:').on_change(self._update_options)
        self._invincible = CheckboxPairWidget('Invincible:').on_change(self._update_options)
        self._unlimited_ammo = CheckboxPairWidget('Unlimited Ammo:').on_change(self._update_options)

        self._map_widget = MapSelection(MAP_NAMES, [])
        self._map_tickets = SliderPairWidget('Tickets:', 1, 300, 75).on_change(self._update_options)
        self._map_era = CheckboxPairWidget('CW/GCW:').on_change(self._update_options)
        self._random_maps = CheckboxPairWidget('Randomize maps:').on_change(self._update_options)

        self._left.addWidget(self._server_name)
        self._left.addWidget(self._server_password)
        self._left.addWidget(self._server_admin_pw)

        self._left.addWidget(Separator())

        self._left.addWidget(self._server_type)
        self._left.addWidget(self._lan)
        self._left.addWidget(self._throttle)
        self._left.addWidget(self._ticks_per_second)
        self._left.addWidget(self._log)

        self._left.addWidget(Separator())

        self._left.addWidget(self._player_limit)
        self._left.addWidget(self._player_count)
        self._left.addWidget(self._player_select)
        self._left.addWidget(self._show_names)
        self._left.addWidget(self._number_of_bots)
        self._left.addWidget(self._bot_difficulty)
        self._left.addWidget(self._heroes)
        self._left.addWidget(self._invincible)
        self._left.addWidget(self._unlimited_ammo)

        self._left.addWidget(Separator())

        self._left.addWidget(self._map_widget)
        self._left.addWidget(self._random_maps)
        self._left.addWidget(self._map_era)
        self._left.addWidget(self._map_tickets)

        self._server_name.second().textChanged.connect(self.on_name_change)
        self._map_widget.on_add(self._new_map)
        self._map_widget.on_remove(self._drop_map)

    def _create_right_column(self):
        self._options = QPlainTextEdit(self.options())
        self._options.setTextInteractionFlags(
            QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse | ~QtCore.Qt.TextEditable)
        self._maps = QTreeWidget()
        self._maps.setColumnCount(3)
        self._maps.setHeaderLabels(['Map name', 'Attacker', 'Defender', 'CW/GCW'])
        self._maps.setColumnWidth(1, 60)
        self._maps.setColumnWidth(2, 60)
        self._maps.setColumnWidth(3, 60)

        self._right.addWidget(self._options)
        self._right.addWidget(Separator())
        self._right.addWidget(self._maps)

    def on_name_change(self):
        self._tab_parent.setTabText(self._tab_id, self._server_name.value())

    def _new_map(self, map_name):
        era = 'CW' if self._map_era.value() else 'GCW'
        item = QTreeWidgetItem([str(map_name), str(self._map_tickets.value()), str(self._map_tickets.value()), era])
        self._maps.addTopLevelItem(item)
        self._update_options()

    def _drop_map(self, index):
        self._maps.takeTopLevelItem(index)
        self._update_options()

    def _update_options(self):
        self._options.setPlainText(self.options())

    def options(self):
        if not self._init:
            return ''

        option = str(' '
                     '/autonet {:s} '
                     '/gamename "{:s}" '
                     '/noaim '
                     '/nointo '
                     '/norender '
                     '/nosound '
                     '/bots {:d} '
                     '/difficulty {:d} '
                     '/playercount {:d} '
                     '/playerlimit {:d} '
                     '/spawn {:d} '
                     '/tps {:d} '
                     '/throttle {:d} '
                     '/win '
                     '/resolution {:d} {:d} '
                     ).format(
            'dedicated' if self._server_type.second().isChecked() else 'pc',
            self._server_name.value(),
            self._number_of_bots.value(),
            self._bot_difficulty.value(),
            self._player_count.value(),
            self._player_limit.value(),
            self._spawn.value(),
            self._ticks_per_second.value(),
            self._throttle.value(),
            int(self._resolution.second().first().text()),
            int(self._resolution.second().second().text()),
        )

        if self._server_password.value():
            option += '/password "' + self._server_password.value() + '" '

        if self._server_admin_pw.value():
            option += '/adminpw "' + self._server_admin_pw.value() + '" '

        if self._lan.value():
            option += '/lan '

        if self._log.value():
            option += '/loginfinalscore '

        if not self._show_names.value():
            option += '/nonames '

        if not self._team_damage.value():
            option += '/noteamdamage '

        if self._player_select.value():
            option += '/sideselect '

        if self._heroes.value():
            option += '/heroes '

        if self._random_maps.value():
            option += '/randomize '

        root = self._maps.invisibleRootItem()
        for i in range(root.childCount()):
            item = root.child(i)
            map_name = item.text(0)
            map_tickets = item.text(1)
            map_era = item.text(3)
            if map_era in MAP_ID[map_name]:
                option += MAP_ID[map_name][map_era] + ' {0} {0} '.format(map_tickets)
            # Map has only one era
            elif len(MAP_ID[map_name]) == 1:
                option += list(MAP_ID[map_name].values())[0] + ' {0} {0} '.format(map_tickets)

        return option
