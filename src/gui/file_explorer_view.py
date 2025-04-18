import os
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QPushButton, QHeaderView
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import Qt, QModelIndex
from datetime import datetime


class FileExplorerView(QWidget):
    def __init__(self, files_data):
        super().__init__()
        self.files_data = files_data
        self.init_ui()
        self.history = []
        self.current_path = "/"  # Početna putanja
        
    def init_ui(self):
     
        layout = QVBoxLayout()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'Size (bytes)', 'Last Modified'])

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setHeaderHidden(False)
        self.tree_view.setAlternatingRowColors(True)

        # Povezujemo dvoklik signal sa metodom za otvaranje fajla
        self.tree_view.doubleClicked.connect(self.open_file)
        try:
            with open("style_tree_view.qss", "r") as f:
                style = f.read()
                print("Stil uspešno učitan!")
        except FileNotFoundError:
            print("Fajl 'style.qss' nije pronađen.")
        except Exception as e:
            print(f"Greška pri čitanju fajla: {e}")

        self.setStyleSheet(style)

        self.back_button = QPushButton("⬅ Back")
        self.back_button.clicked.connect(self.navigate_back)

        # Postavljanje fiksnih širina za druge dve kolone
        self.tree_view.setColumnWidth(1, 100)  # Druga kolona - fiksno 100px
        self.tree_view.setColumnWidth(2, 155)  # Treća kolona - fiksno 155px

        # Povećanje širine prve kolone da preostali prostor bude zauzet
        self.tree_view.setColumnWidth(0, 155)  # Početna širina prve kolone (155px)

        # Automatski prilagoditi širu prozora prema širinama kolona
        total_width = 155 + 100 + 155  # Ukupna širina svih kolona
        self.setMinimumWidth(total_width)  # Povećava širinu prozora prema ukupnoj širini kolona

        layout.addWidget(self.back_button)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

        self.populate_files()
        
    def populate_files(self):
        self.model.removeRows(0, self.model.rowCount())
        for file_name, file_info in self.files_data.items():
            item = QStandardItem(QIcon("icons/file.png"), file_name)
            size_item = QStandardItem(str(file_info['size']))
            formatted_time = self.format_timestamp(file_info['modification_time'])
            mod_time_item = QStandardItem(formatted_time)

            item.setEditable(False)
            size_item.setEditable(False)
            mod_time_item.setEditable(False)

            size_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            mod_time_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)

            self.model.appendRow([item, size_item, mod_time_item])
        


    def format_timestamp(self, timestamp):
        return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M:%S")

    def open_file(self, index: QModelIndex):
        file_name = self.model.itemFromIndex(index).text()
        print(f"Otvaram fajl: {file_name}")

        # Otvori fajl koristeći OS komandu
        if os.name == 'nt':  # Windows
            os.startfile(file_name)
        else:  # Linux / Mac
            subprocess.run(['xdg-open', file_name])  # otvara pomoću podrazumevanog programa

    def navigate_back(self):
        print("Back button clicked (placeholder for future navigation)")
        if self.history:
            last_path = self.history.pop()
            print(f"Vraćam se na: {last_path}")
            self.current_path = last_path
            self.populate_files()
        
class MmainWindow(QMainWindow):
    def __init__(self,files):
        super().__init__()
        self.setWindowTitle("File Explorer (Custom Data)")
        self.file_explorer = FileExplorerView(files)
        self.setCentralWidget(self.file_explorer)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MmainWindow()
    window.show()
    sys.exit(app.exec())
