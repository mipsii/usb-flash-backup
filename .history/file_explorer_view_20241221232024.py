from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QFileSystemModel, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import QDir


class FileExplorerView(QWidget):
    def __init__(self, path=None):
        super().__init__()
        self.path = path if path else QDir.rootPath()
        self.previous_path = None  # Za praćenje prethodnog foldera
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Model za učitavanje fajlova i foldera
        self.model = QFileSystemModel()
        self.model.setRootPath(self.path)

        # TreeView za prikaz
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(self.path))
        self.tree_view.setHeaderHidden(True)

        # Stil i animacija
        self.tree_view.setAnimated(False)
        self.tree_view.setIndentation(20)

        # Klik na folder ili fajl
        self.tree_view.doubleClicked.connect(self.on_double_click)

        # Dugme za navigaciju nazad
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.navigate_back)
        
        layout.addWidget(self.back_button)
        layout.addWidget(self.tree_view)
        self.setLayout(layout)

    def on_double_click(self, index):
        if self.model.isDir(index):
            # Čuvanje trenutnog foldera pre nego što se ide u novi
            self.previous_path = self.path
            self.path = self.model.filePath(index)
            self.tree_view.setRootIndex(index)
        else:
            print("Otvoren fajl:", self.model.filePath(index))

    def navigate_back(self):
        if self.previous_path:
            # Vraćanje na prethodni folder
            self.path = self.previous_path
            self.tree_view.setRootIndex(self.model.index(self.path))
            self.previous_path = None  # Očisti prethodni folder nakon povratka


# Glavni prozor
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("File Explorer")

        # Dodavanje FileExplorerView direktno u centralni widget
        self.file_explorer = FileExplorerView()
        self.setCentralWidget(self.file_explorer)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
