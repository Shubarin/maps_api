import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from dotenv import load_dotenv

from geocoder import get_static_map, get_coordinate, get_full_address

load_dotenv()

LAYERS = {
    'Обычная карта': 'map',
    'Спутниковая карта': 'sat',
    'Спутник с названиями': 'sat,skl',
    'Карта пробок': 'map,trf,skl',
    'Пробки на спутнике': 'sat,trf,skl'
}
START_LL = os.getenv('START_LL')
LAYER = os.getenv('LAYER')
SCREEN_SIZE = os.getenv('SCREEN_SIZE')


class Mapper(QMainWindow):
    def __init__(self):
        super(Mapper, self).__init__()
        uic.loadUi('design.ui', self)
        self.setFixedSize(*map(int, SCREEN_SIZE.split(',')))
        self.ll = START_LL
        self.l = LAYER
        self.points = []
        self.address = None
        self.postal_code = None
        self.layers.addItems(LAYERS.keys())
        self.load_map()
        self.z.valueChanged.connect(self.load_map)
        self.layers.currentTextChanged.connect(self.load_map)
        self.search.clicked.connect(self.set_ll)
        self.clean.clicked.connect(self.clean_history)
        self.indecies.stateChanged.connect(self.set_ll)

    def clean_history(self):
        self.points.clear()
        self.query.setText('')
        self.address = ''
        self.statusBar().clearMessage()
        self.load_map()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            print("Координаты:{}, {}".format(
                event.x(), event.y()))
            x_center, y_center = map(float, self.ll.split(','))
            scale = self.z.value() / 500
            width = 2 * scale
            if event.x() > 600 / 2:
                x = width / 600 * event.x() + x_center
            else:
                x = width * (event.x() / 600) + x_center - width
            y = -width / 430 * event.y() + y_center + 3 * width / 4
            ll = ','.join([str(x), str(y)])
            self.clean_history()
            self.points.append(ll)
            ll, self.address, self.postal_code = get_full_address(ll)
            msg = self.address
            if self.indecies.checkState():
                msg += ', индекс: ' + self.postal_code
            self.statusBar().showMessage(msg)
            self.load_map()
        elif event.button() == Qt.RightButton:
            print("Координаты:{}, {}".format(
                event.x(), event.y()))

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            if event.key() == Qt.Key_Minus:
                if self.z.value() + 1 < 101:
                    self.z.setValue(self.z.value() + 1)
            elif event.key() == Qt.Key_Equal:
                if self.z.value() - 1 > 0:
                    self.z.setValue(self.z.value() - 1)
        x_center, y_center = map(float, self.ll.split(','))
        if event.key() == Qt.Key_Up or event.key() == Qt.Key_Down or \
                event.key() == Qt.Key_Right or event.key() == Qt.Key_Left:
            scale = self.z.value() / 500
            if event.key() == Qt.Key_Up:
                y_center += 2 * scale
            elif event.key() == Qt.Key_Down:
                y_center -= 2 * scale
            elif event.key() == Qt.Key_Right:
                x_center += 2 * scale
            elif event.key() == Qt.Key_Left:
                x_center -= 2 * scale
            self.ll = ','.join([str(x_center), str(y_center)])
            self.load_map()
        self.update()

    def set_ll(self):
        if self.query.text():
            self.ll, self.address, self.postal_code = get_full_address(
                self.query.text())
            self.points.append(self.ll)
            msg = self.address
            if self.indecies.checkState():
                msg += ', индекс: ' + self.postal_code
            self.statusBar().showMessage(msg)
            self.load_map()

    def load_map(self):
        pixmap = QPixmap()
        z = self.z.value()
        l = LAYERS[self.layers.currentText()]
        pixmap.loadFromData(get_static_map(z=z, l=l, ll=self.ll,
                                           points=self.points))
        self.map_img.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Mapper()
    wnd.show()
    sys.exit(app.exec())
