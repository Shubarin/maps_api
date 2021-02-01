import os
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from dotenv import load_dotenv

from geocoder import get_static_map, get_coordinate

load_dotenv()

LAYERS = ['map', 'sat', 'skl']
START_LL = os.getenv('START_LL')


class Mapper(QMainWindow):
    def __init__(self):
        super(Mapper, self).__init__()
        uic.loadUi('design.ui', self)
        self.layers.addItems(LAYERS)
        self.load_map()
        self.z.valueChanged.connect(self.load_map)
        self.layers.currentTextChanged.connect(self.load_map)
        self.search.clicked.connect(self.load_map)

    def keyPressEvent(self, event):
        if int(event.modifiers()) == Qt.ControlModifier:
            # так как нет клавиши Page_Up на клавиатуре
            if event.key() == Qt.Key_Equal:
                if self.z.value() + 1 < 18:
                    self.z.setValue(self.z.value() + 1)
            elif event.key() == Qt.Key_Minus:
                if self.z.value() - 1 > 0:
                    self.z.setValue(self.z.value() - 1)


    def load_map(self):
        pixmap = QPixmap()
        z = self.z.value()
        l = self.layers.currentText()
        ll = START_LL
        if self.query.text():
            ll = get_coordinate(self.query.text())
        pixmap.loadFromData(get_static_map(z=z, l=l, ll=ll))
        self.map_img.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Mapper()
    wnd.show()
    sys.exit(app.exec())