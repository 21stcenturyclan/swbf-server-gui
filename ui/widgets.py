from math import log

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QWidget, QHBoxLayout, QLabel, QSlider, QVBoxLayout, QPushButton, QFrame, \
    QLineEdit, QCheckBox, QStyle


class PairWidget(QWidget):
    def __init__(self, first, second):
        super().__init__()

        self._change_callback = None
        self._box = QHBoxLayout(self)
        self._first = first
        self._second = second
        self._box.addWidget(first, Qt.AlignLeft)
        self._box.addWidget(second, Qt.AlignRight)

    def name(self):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError

    def changed(self):
        if self._change_callback:
            self._change_callback()

    def on_change(self, callback):
        self._change_callback = callback
        return self

    def first(self):
        return self._first

    def second(self):
        return self._second


class CheckboxPairWidget(PairWidget):
    def __init__(self, label, default=False):
        super().__init__(QLabel(label), QCheckBox())

        self.second().setChecked(default)

        self.second().stateChanged.connect(self.changed)

    def name(self):
        return self._first.text()

    def value(self):
        return self._second.isChecked()


class LineEditPairWidget(PairWidget):
    def __init__(self, label, content, pw=False):
        super().__init__(QLabel(label), QLineEdit(content))

        if pw:
            self.second().setEchoMode(QLineEdit.Password)

        self.second().textChanged.connect(self.changed)

    def name(self):
        return self._first.text()

    def value(self):
        return self._second.text()


class SliderPairWidget(PairWidget):
    def __init__(self, label, _min, _max, default, orientation=Qt.Horizontal, edit=True):
        super().__init__(QLabel(label), SliderLabel(_min, _max, orientation, edit))

        self.second().line_edit().setText(str(default))
        self.second().slider().setValue(default)

        self.second().line_edit().textChanged.connect(self.changed)
        self.second().slider().valueChanged.connect(self.changed)

    def name(self):
        return self._first.text()

    def value(self):
        return self._second.value()


class SliderLabel(QWidget):
    def __init__(self, _min, _max, orientation=Qt.Horizontal, edit=True):
        super().__init__()
        self._box = QHBoxLayout(self) if orientation == Qt.Horizontal else QVBoxLayout(self)
        self._slider = QSlider(orientation)
        self._slider.setRange(_min, _max)
        self._slider.setValue(_min)
        self._label = QLineEdit(str(_min))
        self._label.setMaximumWidth((1 + log(_max, 10)) * 10)
        self._label.setAlignment(Qt.AlignCenter)
        self._box.addWidget(self._slider)
        self._box.addWidget(self._label)

        self._label.textChanged.connect(self._text_changed)
        self._slider.valueChanged.connect(self._slider_changed)

    def line_edit(self):
        return self._label

    def slider(self):
        return self._slider

    def value(self):
        return self._slider.value()

    def _slider_changed(self):
        self._label.setText(str(self._slider.value()))

    def _text_changed(self):
        if self._label.text() and self._label.text().isnumeric():
            val = int(self._label.text())
            if self._slider.minimum() <= val <= self._slider.maximum():
                self._slider.setValue(val)


class Separator(QFrame):
    def __init__(self, orientation=Qt.Horizontal):
        super().__init__()
        self.setFrameShape(QFrame.HLine if orientation == Qt.Horizontal else QFrame.VLine)
        self.setFrameShadow(QFrame.Sunken)


class MapSelection(QWidget):
    def __init__(self, available_maps, selected_maps):
        super().__init__()

        self._available = available_maps
        self._selected = selected_maps
        self._hbox = QHBoxLayout(self)
        self._vbox_wrapper = QWidget()
        self._vbox = QVBoxLayout(self._vbox_wrapper)
        self._rbutton = QPushButton(icon=self.style().standardIcon(QStyle.SP_ArrowRight))
        self._lbutton = QPushButton(icon=self.style().standardIcon(QStyle.SP_ArrowLeft))
        self._available_list = QListWidget()
        self._available_list.addItems(available_maps)
        self._selected_list = QListWidget()
        self._selected_list.addItems(selected_maps)
        self._vbox.addWidget(self._rbutton)
        self._vbox.addWidget(self._lbutton)
        self._hbox.addWidget(self._available_list)
        self._hbox.addWidget(self._vbox_wrapper)
        self._hbox.addWidget(self._selected_list)

        self._add_callback = None
        self._remove_callback = None

        self._rbutton.clicked.connect(self._add_clicked)
        self._lbutton.clicked.connect(self._remove_clicked)

    def add(self, index):
        self._selected.append(self._available[index])
        self._selected_list.addItem(self._available[index])

    def _add_clicked(self):
        index = self._available_list.currentItem()
        if self._add_callback and index:
            self._selected.append(index.text())
            self._selected_list.addItem(index.text())
            self._add_callback(index.text())

    def _remove_clicked(self):
        index = self._selected_list.currentIndex().row()
        if self._remove_callback and index >= 0:
            del self._selected[index]
            self._selected_list.takeItem(index)
            self._remove_callback(index)

    def on_add(self, callback):
        self._add_callback = callback

    def on_remove(self, callback):
        self._remove_callback = callback
