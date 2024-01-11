import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
import sqlite3
from UI import addEditCoffeeForm, main

db = sqlite3.connect('data/coffee.sqlite')
sql = db.cursor()


class Edit(QMainWindow, addEditCoffeeForm.Ui_MainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.do)
        self.lineEdit_2.textChanged.connect(self.refresh)

    def refresh(self):
        query = "SELECT * FROM coffee WHERE variety_name = ?"
        name = self.lineEdit_2.text()
        data = sql.execute(query, (name,)).fetchone()
        if not (data is None):
            self.lineEdit_3.setText(data[2])
            self.lineEdit_4.setText(data[3])
            self.lineEdit_5.setText(data[4])
            self.lineEdit_6.setText(data[5])
            self.lineEdit_7.setText(data[6])

    def do(self):
        data = []
        data.append(self.lineEdit_2.text())
        data.append(self.lineEdit_3.text())
        data.append(self.lineEdit_4.text())
        data.append(self.lineEdit_5.text())
        data.append(self.lineEdit_6.text())
        data.append(self.lineEdit_7.text())

        try:
            id = max([i[0] for i in sql.execute("SELECT id FROM coffee").fetchall()]) + 1
        except ValueError:
            id = 0

        if sql.execute("SELECT * FROM coffee WHERE variety_name = ?", (data[0],)).fetchone() is None:
            data = [id] + data
            sql.execute("INSERT INTO coffee VALUES (?, ?, ?, ?, ?, ?, ?)", data)
            db.commit()
        else:
            query = "UPDATE coffee SET degree_of_roasting = ?, ground_or_cereal = ?, flavor_description = ?, price = ?, package_size = ? WHERE variety_name = ?"
            sql.execute(query, data[1:] + [data[0]])
            print(data[1:] + [data[0]])
            db.commit()


class Espresso(QMainWindow, main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.button.clicked.connect(self.do)
        self.button2.clicked.connect(self.edit)

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

    def edit(self):
        edit = Edit(self)
        edit.show()
        

def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Espresso()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())