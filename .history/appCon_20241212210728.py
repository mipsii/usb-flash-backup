#from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QSplitter, QTreeWidget
from PySide6.QtCore import Qt

from usb_list import USBListManager

class Ui_USBBackup:
    """Klasa koja definiše korisnički interfejs."""
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("USB Backup")
        MainWindow.resize(200, 170)
        
        # Centralni widget i layout
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.main_layout = QVBoxLayout(self.centralwidget)
        
        # Glavna labela
        self.label = QLabel("USB nije umetnut", MainWindow)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Status labela
        self.statusLabel = QLabel("", MainWindow)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
         # Splitter za prikaz bekapova i fajlova
        self.splitter = QSplitter(Qt.Orientation.Horizontal, MainWindow)

        # Leva strana: lista backupova
        self.backup_list_widget = QListWidget(MainWindow)
        self.backup_list_widget.setStyleSheet("font-size: 14px;")
        self.backup_list_widget.setFixedWidth(250)
        self.splitter.addWidget(self.backup_list_widget)

        # Desna strana: prikaz fajlova u stilu komandera
        self.file_tree_widget = QTreeWidget(MainWindow)
        self.file_tree_widget.setHeaderLabels(["Naziv fajla", "Veličina", "Datum modifikacije"])
        self.file_tree_widget.setStyleSheet("font-size: 14px;")
        self.splitter.addWidget(self.file_tree_widget)

        self.splitter.setSizes([250, 550])

        self.main_layout.addWidget(self.splitter)

        # Dugme koje će biti skriveno inicijalno
        self.changeButton = QPushButton("Promeni status", MainWindow)
        self.changeButton.setVisible(False)

        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.statusLabel)
        self.main_layout.addWidget(self.changeButton)
       
        
    def usb_inserted(self, serial_number, usb):
        print("usao je u handle") 
        print("add")
        print(f"u insert usb jee { usb }")
        print(f"povrtane inf serijski { serial_number}  i  info  {usb['Label']}")
        print(f"usb info je : { usb }")
        if serial_number:
            self.label.setText(f"USB: { usb['Label'] } Serijski broj: { serial_number }")
            self.statusLabel.setText(f"USB je povezan na {usb['Device']}.")
            self.changeButton.setVisible(True)
        else:
            self.label.setText(f"USB nije umetnut")
            self.statusLabel.setText(f"")
            self.changeButton.setVisible(False)
        
    def usb_remove(self, serial_number):
        # Uklanjanje informacija o USB-u
        self.label.setText("USB nije priključen")
        self.statusLabel.setText("")
        self.changeButton.setVisible(False)
                    
    def update_usb_status(self, serial_number , usb):
        """Ažurira GUI u zavisnosti od statusa umetnutog USB-a."""
        if usb["Is current"]:
            self.label.setText(f"USB: { usb['Label']} (Serijski broj: {serial_number})")
            self.statusLabel.setText("USB je povezan.")
            self.changeButton.setVisible(True)

            if usb["Is registar"]:
                self.changeButton.setText("Backup")
                self.statusLabel.setStyleSheet("color: green;")
                self.statusLabel.setText("USB je registrovan. Spreman za backup.")
            else:
                self.changeButton.setText("Registruj USB")
                self.statusLabel.setStyleSheet("color: red;")
                self.statusLabel.setText("USB nije registrovan. Registrujte ga.")
        else:
            self.label.setText("USB nije priključen")
            self.statusLabel.setText("")
            self.changeButton.setVisible(False)
        
    # def closeEvent(self, event):
    #     """Sakrij prozor sa task bara kada se klikne X."""
    #     event.ignore()
    #     self.hide()
    

