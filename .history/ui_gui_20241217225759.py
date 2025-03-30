from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QSplitter,QListWidgetItem
from PySide6.QtCore import Qt

from usb_list import USBListManager

class Ui_USBBackup:
    """Klasa koja definiše korisnički interfejs."""
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow  # Sačuvaj referencu na MainWindow
        MainWindow.setWindowTitle("USB Backup")
        MainWindow.resize(200, 170)
        self.MainWindow.setMinimumSize(0, 0)
        
        # Centralni widget i layout
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.vertical_layout = QVBoxLayout(self.centralwidget)
        
        # QSplitter za horizontalno deljenje
        self.splitter = QSplitter(Qt.Horizontal)

         # Središnji deo
        self.middle_widget = QWidget(self.splitter)
        self.middle_widget.setFixedWidth(165)
        self.middle_layout = QVBoxLayout(self.middle_widget)
        # Glavna labela
        self.label = QLabel("USB nije umetnut", self.centralwidget)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Status labela
        self.statusLabel = QLabel("", self.centralwidget)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Dugme koje će biti skriveno inicijalno
        self.changeButton = QPushButton("Promeni status", self.centralwidget)
        self.changeButton.setVisible(False)
        self.middle_layout.addWidget(self.label)
        self.middle_layout.addWidget(self.statusLabel)
        self.middle_layout.addWidget(self.changeButton)     

        # Leva strana
        self.left_widget = QWidget(self.splitter)
        self.left_layout = QVBoxLayout(self.left_widget)
        self.left_widget.setFixedWidth(155)
        self.left_widget.setStyleSheet("background-color: #d2ebff;")
        # Dodavanje liste za backup-ove
        self.backup_list = QListWidget(self.left_widget)
        self.left_layout.addWidget(self.backup_list)
        
        # Desna strana
        self.right_widget = QWidget(self.splitter)
        self.right_layout = QVBoxLayout(self.right_widget)
        #self.right_widget.setFixedWidth(200)
        self.right_widget.setStyleSheet("background-color: blue;")
        self.right_label = QLabel("Desni deo", self.right_widget)
        self.right_layout.addWidget(self.right_label)

        # Dodavanje QSplitter u glavni layout
        self.vertical_layout.addWidget(self.splitter)

        # # Dugmad za prikazivanje/sakrivanje levog i desnog prozora
        # self.toggleLeftButton = QPushButton("Prikaži/Sakrij Levo", self.centralwidget)
        # self.toggleLeftButton.clicked.connect(self.toggle_left_widget)
        # self.toggleRightButton = QPushButton("Prikaži/Sakrij Desno", self.centralwidget)
        # self.toggleRightButton.clicked.connect(self.toggle_right_widget)

        # # Dodavanje dugmadi u središnji deo
        # self.middle_layout.addWidget(self.toggleLeftButton)
        # self.middle_layout.addWidget(self.toggleRightButton)
        
        # Početno sakrivanje levog i desnog prozora
        self.left_widget.setVisible(False)
        self.right_widget.setVisible(False)

    def update_usb_info(self, usb_label, status, is_registered=False):
        """Ažurira tekst i dugme u zavisnosti od statusa USB-a."""
        self.label.setText(f"USB: {usb_label}")
        self.statusLabel.setText(status)
        self.statusLabel.setStyleSheet("color: green;" if is_registered else "color: red;")
        self.changeButton.setVisible(True)
        self.changeButton.setText("Backup" if is_registered else "Registruj USB")