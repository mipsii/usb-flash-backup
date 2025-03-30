from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt


class FileExplorerView(QWidget):
    def __init__(self, files_data):
        super().__init__()
        self.files_data = files_data  # Podaci o fajlovima (rečnik)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Kreiranje modela i prikaza
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'Size (bytes)', 'Last Modified'])

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setHeaderHidden(False)

        # Dugme za povratak (za buduću funkcionalnost)
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.navigate_back)

        layout.addWidget(self.back_button)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

        self.populate_files()

    def populate_files(self):
        """Popunjava model sa podacima iz rečnika"""
        self.model.removeRows(0, self.model.rowCount())  # Čisti stari prikaz

        for file_name, file_info in self.files_data.items():
            # Kreiraj red sa tri kolone (ime, veličina, datum modifikacije)
            item = QStandardItem(file_name)
            size_item = QStandardItem(str(file_info['size']))
            mod_time_item = QStandardItem(str(file_info['modification_time']))

            # Postavi da ime fajla nije moguće menjati
            item.setEditable(False)
            size_item.setEditable(False)
            mod_time_item.setEditable(False)

            # Postavi poravnanje (veličina i datum desno)
            size_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            mod_time_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)

            # Dodaj red u model
            self.model.appendRow([item, size_item, mod_time_item])

    def navigate_back(self):
        print("Back button clicked (placeholder for future navigation)")


# Primer podataka o fajlovima
files_data = {
    '1.JPG': {'modification_time': 1432299814.0, 'size': 21827},
    '11050645_1497224103902125_4125995060430789372_n.jpg': {'modification_time': 1734130928.0, 'size': 35524},
    'paprika u medu.docx': {'modification_time': 1439561610.0, 'size': 12984},
    '‚nao.jpg': {'modification_time': 1734099446.0, 'size': 74852},
    '‚nao2.jpg': {'modification_time': 1734099446.0, 'size': 88245}
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Explorer (Custom Data)")

        # Dodavanje FileExplorerView direktno u centralni widget
        self.file_explorer = FileExplorerView(files_data)
        self.setCentralWidget(self.file_explorer)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
