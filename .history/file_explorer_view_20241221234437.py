from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QPushButton
from PySide6.QtGui import QStandardItemModel, QStandardItem, QIcon
from PySide6.QtCore import Qt
from datetime import datetime  # Dodajemo datetime za konverziju vremena


class FileExplorerView(QWidget):
    def __init__(self, files_data):
        super().__init__()
        self.files_data = files_data  # Podaci o fajlovima (rečnik)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'Size (bytes)', 'Last Modified'])

        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setHeaderHidden(False)
        self.tree_view.setAlternatingRowColors(True)

        self.tree_view.setStyleSheet("""
            QTreeView {
                border: 1px solid #ccc;
                background-color: #f8f8f8;
                selection-background-color: #3498db;
                alternate-background-color: #e9e9e9;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 4px;
                font-size: 14px;
                border: 1px solid #2980b9;
            }
            QTreeView::item {
                padding: 5px;
            }
            QTreeView::item:hover {
                background-color: #d6eaf8;
            }
        """)

        self.back_button = QPushButton("⬅ Back")
        self.back_button.clicked.connect(self.navigate_back)

        layout.addWidget(self.back_button)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

        self.populate_files()

    def populate_files(self):
        """Popunjava model sa podacima iz rečnika"""
        self.model.removeRows(0, self.model.rowCount())  # Čisti stari prikaz

        for file_name, file_info in self.files_data.items():
            item = QStandardItem(QIcon("icons/file.png"), file_name)
            size_item = QStandardItem(str(file_info['size']))
            
            # Konvertuj timestamp u čitljiv format
            formatted_time = self.format_timestamp(file_info['modification_time'])
            mod_time_item = QStandardItem(formatted_time)

            item.setEditable(False)
            size_item.setEditable(False)
            mod_time_item.setEditable(False)

            size_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
            mod_time_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)

            self.model.appendRow([item, size_item, mod_time_item])

    def format_timestamp(self, timestamp):
        """Konvertuje timestamp u format dd.MM.yyyy hh:mm:ss"""
        return datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y %H:%M:%S")

    def navigate_back(self):
        print("Back button clicked (placeholder for future navigation)")


files_data = {
    '1.JPG': {'modification_time': 1432299814.0, 'size': 21827},
    'document.docx': {'modification_time': 1734130928.0, 'size': 35524},
    'presentation.pptx': {'modification_time': 1439561610.0, 'size': 12984},
    'photo.jpg': {'modification_time': 1734099446.0, 'size': 74852},
    'music.mp3': {'modification_time': 1734099446.0, 'size': 88245}
}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Explorer (Custom Data)")
        self.file_explorer = FileExplorerView(files_data)
        self.resize(255, 170)
        self.setCentralWidget(self.file_explorer)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
