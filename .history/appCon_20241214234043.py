#from PySide6 import QtCore, QtWidgets
from PySide6.QtWidgets import  QDialog, QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget
from PySide6.QtCore import Qt

from usb_list import USBListManager

class Ui_USBBackup:
    """Klasa koja definiše korisnički interfejs."""
    def setupUi(self, MainWindow):
        MainWindow.setWindowTitle("USB Backup")
        MainWindow.resize(200, 170)
        
        # Centralni widget i layout
        # Centralni widget i layout
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.central_layout = QHBoxLayout(self.centralwidget)  # Horizontalni layout za dva panela

        # Leva strana: lista backup-ova
        self.left_panel = QWidget()
        self.left_layout = QVBoxLayout(self.left_panel)
        
        # Lista backup-ova
        self.backup_list = QListWidget(self.left_panel)
        self.backup_list.addItems(["Backup 1", "Backup 2", "Backup 3"])  # Primer podataka
        self.backup_list.setFixedWidth(111)  # Fiksna širina za listu
        
        # Dodajte listu u layout
        self.left_layout.addWidget(self.backup_list)
        self.left_panel.setLayout(self.left_layout)
        self.left_panel.setVisible(False)

        # Desna strana: informacije o USB uređaju
        self.right_panel = QWidget()
        self.right_layout = QVBoxLayout(self.right_panel)
        
        # Glavna labela za USB
        self.label = QLabel("USB nije umetnut", self.right_panel)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Status labela
        self.statusLabel = QLabel("", self.right_panel)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Dugme koje će biti skriveno inicijalno
        self.changeButton = QPushButton("Promeni status", self.right_panel)
        self.changeButton.setVisible(False)
        
        # Dodajte elemente u desni layout
        self.right_layout.addWidget(self.label)
        self.right_layout.addWidget(self.statusLabel)
        self.right_layout.addWidget(self.changeButton)
        self.right_panel.setLayout(self.right_layout)

        # Dodajte leve i desne panele u glavni layout
        self.central_layout.addWidget(self.left_panel)
        self.central_layout.addWidget(self.right_panel)
       
        
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
    
   