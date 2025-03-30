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
        self.centralwidget = QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)
        self.vertical_layout = QVBoxLayout(self.centralwidget)
        
        # Glavna labela
        self.label = QLabel("USB nije umetnut", MainWindow)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Status labela
        self.statusLabel = QLabel("", MainWindow)
        self.statusLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Dugme koje će biti skriveno inicijalno
        self.changeButton = QPushButton("Promeni status", MainWindow)
        self.changeButton.setVisible(False)

         # Lista priključenih USB uređaja
        #self.usbList = QListWidget(MainWindow)
        # self.usbList.setFixedHeight(15)  # Ograničavamo visinu na prikaz 2-3 uređaja
        # self.usbList.setVisible(False)
        # self.usbList.setStyleSheet("font-family: 'Courier New'; font-size: 14px;")
        #self.usbList = self.usb_list_widget  # Dodeljivanje usb_list_widget koji je prosleđen
        #self.vertical_layout.addWidget(self.usbList)  # Dodaj usb listu u layout
        # Dodajemo elemente u layout
        self.vertical_layout.addWidget(self.label)
        self.vertical_layout.addWidget(self.statusLabel)
        self.vertical_layout.addWidget(self.changeButton)
       
        
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
    

