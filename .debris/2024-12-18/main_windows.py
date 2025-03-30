import sys
from PyQt6.QtWidgets import QApplication,QMainWindow 
from PyQt6.QtCore import QTimer
from appCon import Ui_USBBackup, UsbInfoPopup  # Importujte generisani UI kod
from usb_serial import USBSerialManager
from usb_folder import USBFolderManager


 
class MainWindow( QMainWindow):
    def __init__(self):
        super().__init__()
        self.serial_number = None
        self.usb_name = None
        
        self.usb_serial = USBSerialManager()
        self.usb_folder = USBFolderManager(self.serial_number, self.usb_name)
        self.handle_usb_event()

        
        # Inicijalizacija korisničkog interfejsa
        self.ui = Ui_USBBackup()
        self.ui.setupUi(self)
        
        # Povezujemo dugme sa akcijom
        self.ui.changeButton.clicked.connect(self.on_change_button_clicked)
        
        # Postavljamo timer za simulaciju umetanja USB-a
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_usb_inserted)
        self.timer.start(2000)  # Proverava na svakih 2 sekunde

    def check_usb_inserted(self):
        """Simulacija detekcije umetanja USB-a i statusa registracije."""
        usb_name = "Test USB"
        serial_number = "1234-5678"
        is_registered = True  # Simulirano stanje, možete promeniti na False za testiranje
        
        self.update_usb_status(usb_name, serial_number, is_registered)

    def update_usb_status(self, usb_name, serial_number, is_registered):
        """Ažurira GUI u zavisnosti od statusa umetnutog USB-a."""
        if usb_name:
            self.ui.label.setText(f"USB: {usb_name} (Serijski broj: {serial_number})")
            self.ui.statusLabel.setText("USB je povezan.")
            self.ui.changeButton.setVisible(True)

            if is_registered:
                self.ui.changeButton.setText("Backup")
                self.ui.statusLabel.setStyleSheet("color: green;")
                self.ui.statusLabel.setText("USB je registrovan. Spreman za backup.")
            else:
                self.ui.changeButton.setText("Registruj USB")
                self.ui.statusLabel.setStyleSheet("color: red;")
                self.ui.statusLabel.setText("USB nije registrovan. Registrujte ga.")
        else:
            self.ui.label.setText("USB nije priključen")
            self.ui.statusLabel.setText("")
            self.ui.changeButton.setVisible(False)

    def on_change_button_clicked(self):
        """Reakcija na klik dugmeta za registraciju ili backup."""
        if self.ui.changeButton.text() == "Backup":
            # Logika za backup
            self.ui.statusLabel.setText("Pokrenut backup...")
        else:
            # Logika za registraciju USB-a
            self.ui.statusLabel.setText("Registracija USB-a...")

# Pokretanje aplikacije
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
    
   
            
    def handle_usb_event(self):
        """Funkcija za pokretanje nakon detekcije USB-a."""
        serial_number, mount_point, usb_name = self.usb_serial.get_usb_serial()
        print(serial_number)
        if serial_number:
            self.handle_usb_insertion(serial_number, usb_name )
            print("izracunava")       
        else:
            print("USB nije detektovan ili serijski broj nije pronađen.")
        backup_files_path = self.usb_folder.find_usb_folder(serial_number)
        print(f"pre synh  {backup_files_path}")
        
        print("usao je u handle")
        #synhrofile(mount_point, backup_files_path)
        
    def handle_usb_insertion(self, serial_number, usb_name):
        """Obrađuje ubacivanje USB-a i sinhronizuje fajlove."""
        self.backup_dir = self.usb_folder.find_usb_folder(serial_number)
        if not self.backup_dir:
            if message_box("USB nije registrovan. Želite li napraviti backup?") == QMessageBox.StandardButton.Yes:
                # Kreiraj novi folder sa serijskim brojem USB-a u izabranom folderu
                print(" kreira se folder za usb ")
                self.usb_folder.create_usb_folder(serial_number, usb_name)          
        return 
