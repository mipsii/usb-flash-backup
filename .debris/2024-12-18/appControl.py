import random
from PySide6 import QtWidgets
from PySide6.QtWidgets import QLabel, QPushButton

from PySide6.QtCore import QTimer

class Ui_USBBackup(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.filePopup = FilePopup(self)  # Kreirajte instancu FilePopup prozora jednom

        self.setWindowTitle("USB Backup")
        self.resize(150, 150)

        # Centralni widget i layout za centralizaciju elemenata
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.vertical_layout = QtWidgets.QVBoxLayout(self.centralwidget)

        # Glavna labela koja će pokazivati naziv USB uređaja ili poruku o stanju
        self.label = QtWidgets.QLabel("USB It is not insert", self)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Drugi label koji će prikazivati status operacija (npr. unmount ili registroivan  ili backup)
        self.statusLabel = QLabel("", self)
        self.statusLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        # Dugme ispod koje je inicijalno skriveno
        self.changeButton = QPushButton("Change text", self)
        self.changeButton.setVisible(False)

        # Dodavanje elemenata u layout
        self.vertical_layout.addWidget(self.label)
        self.vertical_layout.addWidget(self.statusLabel)
        self.vertical_layout.addWidget(self.changeButton)

        # Kreiramo instancu pop-up prozora
        self.changeButton.clicked.connect(self.show_file_popup)

        # Timer za periodičnu proveru USB-a
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_usb_inserted)
        self.timer.start(2000)  # Provera svakih 2000 ms (2 sekunde)
        
    
    def check_usb_inserted(self):
        """Funkcija koja proverava da li je USB umetnut."""
        # Simulacija umetanja USB-a (u pravoj aplikaciji, proverite USB putem OS biblioteke)
        usb_name = self.detect_usb()  # Ovo bi trebalo da bude stvarna detekcija
        self.update_usb_status(usb_name, random.choice([True, False]))

    def detect_usb(self):
        """Simulira detekciju umetanja USB-a. Ovde zamenite sa stvarnom proverom."""
        # Primer detekcije (ovde možete staviti stvarnu logiku za detekciju USB-a)
        # U ovom slučaju, vraćamo ime USB-a ako je detektovan, u suprotnom None
        return "Valid USB"  # ili None ako USB nije umetnut

    def update_usb_status(self, usb_name, is_registered):
        """Ažuriraj status USB-a (da li je priključen, registrovan ili je potrebno uraditi backup)."""
        if usb_name:
            self.label.setText(f"USB: {usb_name}")
            self.statusLabel.setText("USB je povezan.")
            self.changeButton.setVisible(True)
            if is_registered:
                self.changeButton.setText("Backup")
                self.statusLabel.setStyleSheet("color: green;")
                self.statusLabel.setText("Do you want backup")
            else:
                self.changeButton.setText("Registruj USB")
                self.statusLabel.setText("USB nije registrovan. Registrujte ga.")
        else:
            self.label.setText("USB nije priključen")
            self.statusLabel.setText("")
            self.changeButton.setVisible(False)

    def on_usb_inserted(self, usb_name):
        """Simulacija USB umetanja, ažuriranje statusa."""
        # Pretpostavljamo da je USB sada povezan, proveravamo da li je registrovan ili ne
        if usb_name:
            is_registered = self.check_if_registered(usb_name)
            self.update_usb_status(usb_name, is_registered)

    def check_if_registered(self, usb_name):
        """Proverava da li je USB registrovan."""
        return usb_name == "Valid USB"  # Primer uslova za registrovan USB

    def show_file_popup(self):
        """Otvara pop-up prozor za fajlove."""
        self.filePopup.show_files()
        pass
    

#Popup windows
from PySide6 import QtWidgets, QtCore

class FilePopup(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fajlovi")
        self.setFixedSize(200, 300)

        # Glavni layout za pop-up prozor
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # Kreiramo sekcije sa hover efektom
        self.create_file_section("New files", "green", ["Novi_fajl1.txt", "Novi_fajl2.txt"])
        self.create_file_section("Modification files", "blue", ["Izmenjen_fajl1.txt", "Izmenjen_fajl2.txt"])
        self.create_file_section("Deleted files", "coral", ["Obrisan_fajl1.txt", "Obrisan_fajl2.txt"])

        # Horizontalni layout za dugmad "Cancel" i "OK"
        self.button_layout = QtWidgets.QHBoxLayout()
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.ok_button = QtWidgets.QPushButton("OK")
        self.button_layout.addWidget(self.cancel_button)
        self.button_layout.addWidget(self.ok_button)

        self.cancel_button.clicked.connect(self.reject)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addLayout(self.button_layout)

    def create_file_section(self, title, color, file_list):
        """Kreira sekciju sa dugmetom koje prikazuje fajlove pri kliku."""
        # Labela za naslov sekcije
        label = QtWidgets.QLabel(title, self)
        label.setStyleSheet("font-weight: bold;")

        # Dugme koje prikazuje fajlove pri kliku
        show_files_button = QtWidgets.QPushButton(f"Show {title.lower()}", self)
        show_files_button.setStyleSheet(f"background-color: {color};")
        
        # Povezivanje dugmeta sa funkcijom za prikazivanje fajlova
        show_files_button.clicked.connect(lambda: self.show_files_list(file_list, title))

        # Layout za sekciju
        section_layout = QtWidgets.QVBoxLayout()
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(5)
        section_layout.addWidget(label)
        section_layout.addWidget(show_files_button)

        # Dodavanje sekcije u glavni layout
        self.layout.addLayout(section_layout)

    def show_files_list(self, file_list, title):
        """Prikazuje iskačući prozor sa listom fajlova."""
        # Kreiranje prozora sa listom fajlova
        list_dialog = QtWidgets.QDialog(self)
        list_dialog.setWindowTitle(f"Fajlovi u kategoriji: {title}")
        list_dialog.setFixedSize(250, 300)
        
        # Glavni layout za prikazivanje liste fajlova
        list_layout = QtWidgets.QVBoxLayout(list_dialog)
        
        list_widget = QtWidgets.QListWidget(list_dialog)
        for file_name in file_list:
            list_widget.addItem(file_name)
        
        list_layout.addWidget(list_widget)

        # Dugme za zatvaranje prozora sa listom fajlova
        close_button = QtWidgets.QPushButton("Zatvori")
        close_button.clicked.connect(list_dialog.close)
        list_layout.addWidget(close_button)

        list_dialog.exec()
    
    def show_files(self):
        """Prikazuje fajlove u sekcijama."""
        self.exec()  # Otvara pop-up prozor


# Primer za testiranje
if __name__ == "__main__":

    app = QtWidgets.QApplication([])
    window = Ui_USBBackup()
    window.show()
    app.exec()
