import sys
import os
import pandas as pd
import datetime
from PyQt5.QtCore import  Qt
from PyQt5.QtGui import QImage, QImageReader, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QScrollArea, QGridLayout, QPushButton, QSizePolicy, QVBoxLayout, \
    QLabel, QTabWidget, QFormLayout, QLineEdit, QFileDialog, QTableWidget, QHeaderView, QTableWidgetItem, \
    QAbstractItemView


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "CompAss"
        self.left = 200
        self.top = 200
        self.width = 1400
        self.height = 800

        self.mainLayout = QGridLayout(self)

        self.load_section = QWidget()
        self.load_section.main_load_layout = QFormLayout(self.load_section)
        self.load_section.setStyleSheet("background-color:rgb(100,150,200")
        self.set_form_section()

        self.history_section = QWidget()
        self.history_section.main_history_layout = QGridLayout(self.history_section) # ustawienie layoutu okna historii
        self.history_section.setStyleSheet("background-color:rgb(20, 20, 20);")
        self.set_history_section() #Sekcja w której użytkownik wybiera plik
        self.set_info_section() #Informacje dotyczące wybranego pliku, wczytywanie i usuwanie z historii, dodanie do ważnych
        self.set_message_section() #Komunikat przy  wykonaniu akcji usunięcia lub dodania pliku do ważnych

        self.sections = QTabWidget()
        self.sections.addTab(self.load_section, "Wczytaj plik")
        self.sections.addTab(self.history_section, "Historia")
        self.mainLayout.addWidget(self.sections,0,0)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)
        self.read_from_csv()
        self.set_history_grid()
        self.show()

    def set_history_section(self):
        history_section = self.history_section
        history_section.history_view = QScrollArea()
        history_section.history_view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        history_section.history_view.setWidgetResizable(True)
        self.content_area = QWidget()
        self.content_area.layout = QGridLayout(self.content_area)
        self.content_area.layout.setSpacing(20)
        history_section.history_view.setWidget(self.content_area)
        history_section.history_view.setStyleSheet("background-color:rgb(100,100,100);")
        history_section.history_view.setMinimumWidth(500)
        history_section.history_view.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        history_section.main_history_layout.addWidget(history_section.history_view,1,0)
    def set_info_section(self):
        history_section = self.history_section
        history_section.info_view = QWidget()
        history_section.info_view.info_layout = QVBoxLayout(history_section.info_view)
        history_section.info_view.setStyleSheet("background-color:rgb(150, 200, 150);")
        history_section.info_view.setFixedWidth(350)
        history_section.info_view.setMinimumHeight(500)
        history_section.info_view.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        history_section.main_history_layout.addWidget(history_section.info_view,1,1)

        history_section.info_view.index = QLabel(history_section.info_view)
        history_section.info_view.important = QPushButton()
        history_section.info_view.important.setText("★")
        history_section.info_view.important.setFixedSize(50,50)
        history_section.info_view.important.setStyleSheet("background-color:rgb(200,200,0); font-size:30px;")
        history_section.info_view.info_layout.addWidget(history_section.info_view.important,alignment=Qt.AlignRight)

        history_section.info_view.table = QTableWidget()
        history_section.info_view.info_layout.addWidget(history_section.info_view.table)
        history_section.info_view.table.setColumnCount(2)
        history_section.info_view.table.setRowCount(3)
        history_section.info_view.table.verticalHeader().setVisible(False)
        history_section.info_view.table.horizontalHeader().setVisible(False)
        history_section.info_view.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        history_section.info_view.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        history_section.info_view.table.setStyleSheet("* {font-family: Arial; font-size: 20px; color: darkgreen; border-radius: 20px;}")
        history_section.info_view.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        history_section.info_view.table.setSelectionMode(QAbstractItemView.NoSelection)
        history_section.info_view.table.setFixedHeight(300)

        history_section.info_view.table.setItem(0,0,QTableWidgetItem("Nazwa pliku: "))
        history_section.info_view.table.setItem(1,0,QTableWidgetItem("Data utworzenia: "))
        history_section.info_view.table.setItem(2,0,QTableWidgetItem("Ścieżka: "))
        history_section.info_view.confirm = QPushButton("Wczytaj")
        history_section.info_view.remove_from_history = QPushButton("Usuń z historii")
        history_section.info_view.info_layout.addWidget(history_section.info_view.confirm,alignment=Qt.AlignCenter)
        history_section.info_view.info_layout.addWidget(history_section.info_view.remove_from_history, alignment=Qt.AlignCenter)
    def set_message_section(self):
        history_section = self.history_section
        history_section.message_view = QWidget()
        history_section.message_view.message_layout = QVBoxLayout(history_section.message_view)
        history_section.message_view.message_layout.addWidget(QLabel("Komunikat"))
        history_section.message_view.setStyleSheet("background-color:rgb(200, 140, 40);")
        history_section.message_view.setFixedHeight(50)
        history_section.message_view.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        history_section.main_history_layout.addWidget(history_section.message_view,2,0,1,2)

    def set_form_section(self):
        self.load_section.file_name = QLineEdit()
        self.load_section.file_upload = QPushButton("Prześlij plik zdjęcia do wczytania")
        self.load_section.main_load_layout.addRow("Nazwa pliku", self.load_section.file_name)
        self.load_section.main_load_layout.addRow("Przesłane zdjęcie", self.load_section.file_upload)
        self.load_section.file_upload.clicked.connect(lambda: self.send_file())
        self.load_section.label_for_image = QLabel(self.load_section)
        self.load_section.main_load_layout.addWidget(self.load_section.label_for_image)
        self.load_section.confirm_button = QPushButton("Zatwierdź")
        self.load_section.main_load_layout.addRow("Prześlij plik", self.load_section.confirm_button)
        self.load_section.confirm_button.clicked.connect(lambda: self.save_to_csv())
    def send_file(self):
        self.opened_file_name = QFileDialog.getOpenFileName()
        self.load_section.file_upload.setText("Załadowano zdjęcie pliku")
        image = QPixmap(self.opened_file_name[0])
        self.load_section.label_for_image.setPixmap(image.scaled(400,400))
    def save_to_csv(self):
        try:
            data = [[self.load_section.file_name.text(),1,self.opened_file_name[0],datetime.datetime.now().strftime("%Y-%m-%d"),0]]
            print(data)
            df_row = pd.DataFrame(data,columns =["name","num_of_birds","path","date","important"])
            try:
                df = pd.read_csv("data/history.csv")
                df_row.to_csv("data/history.csv",mode='a',index=True, header=False)
            except FileNotFoundError:
                if not os.path.exists("data/"):
                    os.mkdir("data/")
                df_row.to_csv("data/history.csv",index=True, header=True)
        except Exception as e:
            print(e)

    def read_from_csv(self):
        self.widget_list = []
        try:
            data = pd.read_csv("data/history.csv")
            for index, rows in data.iterrows():
                self.widget_list.append(self.prepare_history_tile(rows['name'],rows['path'],rows['important'],rows['date'],index))
        except Exception as e:
            print(e)

    def prepare_history_tile(self, title, path, important, date, index):
        history_tile = QPushButton()
        history_tile.setStyleSheet("* {background-color:rgb(150, 200, 150); border-radius: 15px;}")
        history_tile.setFixedSize(200, 200)
        history_tile.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        history_tile.index = index

        label_for_image = QLabel(history_tile)
        label_for_image.move(15, 25)

        title_label = QLabel(history_tile)
        title_label.setText(str(title))
        title_label.setFixedSize(200,50)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("background-color:rgb(150, 200, 180); font-family: Arial; font-size: 20px; color: white; border: 0px solid black;")
        title_label.move(title_label.x(), 150)

        set_as_favourite = QLabel(history_tile)
        set_as_favourite.setProperty("class", important)
        set_as_favourite.move(180,-5)
        set_as_favourite.setFixedSize(30,30)
        set_as_favourite.setStyleSheet('* {display: none; border-radius: 0px;} QLabel[class="1"] {background-color:rgb(30,30,180)}')

        image = QPixmap(path)
        aspect = image.scaled(170,170, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        label_for_image.setPixmap(aspect)
        history_tile.clicked.connect(lambda: self.set_info_content(title, path, date))

        return history_tile

    def set_history_grid(self):
        row_count = 3
        current_col = 0
        current_row = 0
        for widget in self.widget_list:
            self.content_area.layout.addWidget(widget,current_col,current_row)
            print(current_row,current_col)
            if current_row < row_count:
                current_row += 1
            else:
                current_row = 0
                current_col += 1
        #self.history_section.history_view.layout.addWidget(self.widget_list[1],2,0)
        #self.history_section.history_view.layout.addWidget(self.widget_list[3],2,1)
    def set_info_content(self, title,path,date):
        try:

            self.history_section.info_view.table.setItem(0,1,QTableWidgetItem(str(title)))
            self.history_section.info_view.table.setItem(1,1,QTableWidgetItem(str(date)))
            self.history_section.info_view.table.setItem(2,1,QTableWidgetItem(str(path)))
        except Exception as e:
            print(e)

app = QApplication(sys.argv)
exe = MainWindow()
app.exec_()