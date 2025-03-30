from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt



class FileExplorerView(QWidget):
    def __init__(self, files_data):
        super().__init__()
        self.files_data = files_data  # Podaci o fajlovima (rečnik)
        self.previous_path = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Kreiranje modela i prikaza
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'Size', 'Last Modified'])

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setHeaderHidden(False)

        # Dugme za povratak
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.navigate_back)

        layout.addWidget(self.back_button)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

        self.populate_files()

    def populate_files(self):
        """Popunjava model sa podacima o fajlovima"""
        for file_name, file_info in self.files_data.items():
            item = QStandardItem(file_name)
            size_item = QStandardItem(str(file_info['size']))
            mod_time_item = QStandardItem(str(file_info['modification_time']))
            item.setEditable(False)  # Ne dozvoljava editovanje imena fajla

            self.model.appendRow([item, size_item, mod_time_item])

    def navigate_back(self):
        """Navigacija unazad (ako ima prethodni folder)"""
        if self.previous_path:
            print("Vraćam se na prethodni folder:", self.previous_path)
            self.previous_path = None


# Primer podataka o fajlovima
files_data = {
    '1.JPG': {'modification_time': 1432299814.0, 'size': 21827},
    '11050645_1497224103902125_4125995060430789372_n.jpg': {'modification_time': 1734130928.0, 'size': 35524},
    'paprika u medu.docx': {'modification_time': 1439561610.0, 'size': 12984},
    '‚nao.jpg': {'modification_time': 1734099446.0, 'size': 74852},
    '‚nao2.jpg': {'modification_time': 1734099446.0, 'size': 88245}
}

# Glavni prozor
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Explorer")

        # Dodavanje FileExplorerView direktno u centralni widget
        self.file_explorer = FileExplorerView(files_data)
        self.setCentralWidget(self.file_explorer)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
