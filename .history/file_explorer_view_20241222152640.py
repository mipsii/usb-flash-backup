import os
import subprocess
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import Qt, QModelIndex
from datetime import datetime


class FileExplorerView(QWidget):
    def __init__(self, files_data):
        super().__init__()
        self.files_data = files_data
        self.init_ui()

    def init_ui(self):
         # Pozicija trenutnog prozora
        current_x = self.x()  # Trenutna X pozicija
        current_y = self.y()  # Trenutna Y pozicija

        print(f"koordinate su ...{current_x}....{current_y}")
        # Postavi novi prozor 33px levo od trenutnog
        self.setGeometry(current_x - 1, current_y, 300,300)
        layout = QVBoxLayout()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'Size (bytes)', 'Last Modified'])

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setHeaderHidden(False)
        self.tree_view.setAlternatingRowColors(True)
        
        # Povezujemo dvoklik signal sa metodom za otvaranje fajla
        self.tree_view.doubleClicked.connect(self.open_file)

        self.tree_view.setStyleSheet("""
            QTreeView {
        border: 1px solid #ddd;
        background-color: #8b9dc3;
        selection-background-color: #4CAF50;  /* zelena boja selekcije */
        alternate-background-color: #8b9dc3;
        font-size: 14px;
        color: #333;
        border-radius: 7px;
        }

        QTreeView::item {
            padding: 8px;
            border-radius: 4px;
            background-color: transparent;
            transition: background-color 0.2s ease-in-out;
        }

        QTreeView::item:hover {
            background-color: #e0f7fa;  /* svetlo plava boja pri hover */
        }

        QHeaderView::section {
            background-color: #4CAF50;  /* zelena boja za zaglavlja */
            color: white;
            padding: 8px;
            font-size: 16px;
            font-weight: bold;
            border: none;
            border-radius: 4px;
            text-align: left;
            transition: background-color 0.3s ease-in-out;
        }

        QHeaderView::section:hover {
            background-color: #45a049;  /* tamnija zelena pri hover */
        }

        QTreeView::branch:has-sibling {
            border-image: url(':/branch.png') 0 stretch stretch;
            background: transparent;
        }

        QTreeView::indicator:checked {
            background-color: #4CAF50;
            border-radius: 4px;
        }

        QTreeView::indicator:unchecked {
            background-color: #ccc;
            border-radius: 4px;
        }
        """)

        self.back_button = QPushButton("⬅ Back")
        self.back_button.clicked.connect(self.navigate_back)

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
