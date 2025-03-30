from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QStackedWidget, QListWidget

class USBBackupUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB Backup")
        self.resize(400, 300)
        
        self.layout = QVBoxLayout(self)
        self.stack = QStackedWidget(self)
        self.layout.addWidget(self.stack)

        # Glavni prozor
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        self.label = QLabel("USB nije umetnut", self.main_widget)
        self.status_label = QLabel("", self.main_widget)
        self.change_button = QPushButton("Promeni status", self.main_widget)
        self.change_button.setVisible(False)
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.status_label)
        self.main_layout.addWidget(self.change_button)
        self.stack.addWidget(self.main_widget)

        # Backup lista
        self.backup_widget = QWidget()
        self.backup_layout = QVBoxLayout(self.backup_widget)
        self.backup_list = QListWidget(self.backup_widget)
        self.backup_layout.addWidget(self.backup_list)
        self.stack.addWidget(self.backup_widget)
