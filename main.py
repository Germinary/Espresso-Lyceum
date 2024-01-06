import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sqlite3

db = sqlite3.connect('coffee.sqlite')
sql = db.cursor()


class Espresso(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        
        self.button.clicked.connect(self.do)

    def get_data(self, name):
        data = sql.execute("SELECT * FROM coffee WHERE variety_name = ?", (name,)).fetchone()
        return data

    def place_data(self, data):
        data = [str(i) for i in data]
        self.label_1.setText('ID: ' + data[0])
        self.label_2.setText('Название сорта: ' + data[1])
        self.label_3.setText('Степень обжарки: ' + data[2])
        self.label_4.setText('Молотый/в зернах: ' + data[3])
        self.label_5.setText('Описание вкуса: ' + data[4])
        self.label_6.setText('Цена: ' + data[5])
        self.label_7.setText('Объем упаковки: ' + data[6])

    def do(self):
        name = self.lineEdit.text()
        data = self.get_data(name)
        try:
            self.place_data(data)
        except TypeError:
            self.place_data(['N/A'] * 7)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Espresso()
    window.show()
    sys.exit(app.exec_())