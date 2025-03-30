import asyncio
import sys
from PySide6.QtWidgets import QMainWindow, QApplication
import pyudev
from appCon import Ui_USBBackup
from PySide6.QtGui import QColor, QBrush, Qt
from PySide6.QtWidgets import QListWidgetItem
from file_change import FileChangeManager

from usb_list import USBListManager

class MainWindow(QMainWindow):
    def __init__(self, usb_class):
        super().__init__()
        self.usb_class = usb_class
             
        # Inicijalizacija korisničkog interfejsa
        self.ui = Ui_USBBackup()
        self.ui.setupUi(self)
        self.check_connected_usb_devices()
        print("u main u je ")
        self.managerList = USBListManager(self, self.usb_class)
        self.ui.usbList = self.managerList.usb_list_widget  # Pravilno dodeljivanje usb_list_widget
        self.ui.vertical_layout.addWidget(self.ui.usbList)
        # Povezujemo dugme sa akcijom
        self.ui.changeButton.clicked.connect(self.on_change_button_clicked)
        
                
    def handle_usb_event(self, action, deviceID):
        """Rukuje događajem umetanja ili uklanjanja USB-a."""
        print("promena sa  usb")
        print(action, deviceID )
        
        if action == "add":
            device = self.usb_class.usb_device.get_connected_usb_devices(deviceID)
            print(f"usb je :::: {device}")
                       
            # for file in usb_files:
            #     pass
                #self.modern_popup.modified_files_list.addWidget(file)
            #print(f" usb je { usb_files }")
            # Preuzimanje informacija o uređaju na osnovu serijskog broja
            serial_number = device["Serial number"]
            usb = self.usb_class.usb_info.get(serial_number)
            #print(f" registrovan  { usb.get("Is registar")}")
            # Provera da li je uređaj registrovan
            if  not serial_number in self.usb_class.usb_info:
                print("USB uređaj nije registrovan. Pokrećem registraciju.")
                # Registracija USB uređaja
                usb_label = device.get("Label")
                self.usb_class.usb_folder.create_usb_folder(usb_label, serial_number)
                
                # Dodavanje informacija u `usb_info`
                print(f"USB uređaj {serial_number} je sada registrovan.")
            
            # Ažuriranje GUI-ja
            mount = device.get("Mount Point")
            self.usb_class.add_usb_info(serial_number, device.get(("Label")), deviceID, 
                                        mount, 
                                        register_bool = True, current_bool = True, active_bool = True)
            print(f"ubacen usb je   { self.usb_class.usb_info[serial_number]}")
            self.usb_class.update_current_usb(serial_number)
            self.ui.usb_inserted(serial_number, self.usb_class.usb_info[serial_number])
            try:
                loop = asyncio.get_running_loop()
                asyncio.create_task(self.analyz_files())
            except RuntimeError as e:
                print(f"Greška: asyncio petlja nije aktivna - {e}")
             
        elif action == "remove":
            # Uklanjanje informacija o USB-u
            device = self.usb_class.usb_device.find_device(device = deviceID)
            if device:
                serial_number,_ = device
                print(f"usb je izvuceno i serijski je  {serial_number}")
                #asyncio.create_task(self.file_change.clear_changes())
                if self.file_change.popup is not None:
                    self.file_change.popup.reject()
                    #asyncio.create_task(self.file_change.clear_changes())
                    self.file_change.popup = None  # Resetuje referencu
                    print("USB je uklonjen. Popup zatvoren.")
                self.usb_remove(serial_number)
            else:
                print("laznjak")

        if device:    
            self.ui.update_usb_status(serial_number, self.usb_class.usb_info[serial_number])
            self.add_usb()
   
    async def analyz_files(self):
        sserial_number, details = self.usb_class.usb_info_manager.get_current_usb_info()
        usb_backup = details.get("Device")
        backup_path = self.usb_class.usb_folder.find_usb_folder(sserial_number)
        print(f" usb putanja  je { mount }")
        print(f"putanja cakup je { usb_backup }")
        self.file_change = FileChangeManager( usb_backup, backup_path)
        print(f"kreiran file_change")
        await self.file_change.analyze_changes()
        
    def usb_remove(self, serial_number):
        # Uklanjanje informacija o USB-u
        self.usb_class.usb_info_manager.remove_device(serial_number)
        #print(f"usb info je : {self.usb_info}")
        self.managerList.update_usb_list()
        self.ui.usb_remove(serial_number)
    
    def on_change_button_clicked(self):
        """Reakcija na klik dugmeta za registraciju ili backup."""
        
        if self.ui.changeButton.text() == "Backup":
            # Logika za backup
            self.ui.statusLabel.setText("Pokrenut backup...")
            
            # usb_backup = details.get("Device")
            # mount = details.get('Mount Point')
            # print(f" usb putanja  je { mount }")
            # print(f"putanja cakup je { usb_backup }")
            # FileChangeManager( usb_backup, mount)
            self.file_change.initiate_backup_with_popup()
        
        else:
            # Logika za registraciju USB-a
            self.ui.statusLabel.setText("Registracija USB-a...")
            sserial_number, details = self.usb_class.usb_info_manager.get_current_usb_info()
            print(f" klik je na koji { sserial_number }  i  { details}")
            label = details["Label"]
            self.usb_class.usb_folder.create_hidden_file_with_serial_number(label, sserial_number)
            self.usb_class.usb_info_manager.update_usb_info(sserial_number, {"Is registar": True})
    
    def add_usb(self):
        """Dodaje USB uređaj u listu."""
        
        self.managerList.update_usb_list()
       
        #self.ui.usbList.itemClicked.connect(self.on_item_clicked)
        # Ako veza nije već postavljena, postavi signal
        if not hasattr(self, "_item_clicked_connected") or not self._item_clicked_connected:
            self.ui.usbList.itemClicked.connect(self.on_item_clicked)
            self._item_clicked_connected = True

    def on_item_clicked(self, item):
        """Postavlja kliknutu stavku kao trenutnu."""
        # Dohvati serijski broj iz stavke
        serial_usb = item.data(Qt.UserRole)
        print(f" klik na    {serial_usb}")
        # Ažuriraj current status u usb_info
        for serial, usb in self.usb_class.usb_info.items():
            usb["Is_current"] = (serial == serial_usb)   # Postavi trenutni samo za kliknuti uređaj
           
         # Izvrši dodatne akcije (npr. prikaz detalja o USB-u)
        self.ui.usb_inserted(serial, usb)
        
        # Ponovo prikaži stavke kako bi se boje ažurirale
        self.add_usb()
    
    
    def update_usb_list(self):
        """Ažurira QListWidget listu sa USB uređajima, sa odgovarajućim bojama za status."""
        self.usb_list_widget.clear()  # Obrisati sve stavke pre ažuriranja

        for serial_number, usb in self.usb_class.usb_info.items():
            print(f"Učitavanje liste: {serial_number}")
            item_text = f"{usb['Label']} - {serial_number}"
            list_item = QListWidgetItem(item_text)

            # Čuvaj serijski broj u stavci da bi ga koristio kasnije
            list_item.setData(0, serial_number)

            if not usb["Is_active"]:
                list_item.setFlags(list_item.flags() & ~Qt.ItemIsEnabled)  # Onemogućite stavku

            # Dodavanje boje pozadine na osnovu statusa
            if usb.get("Is current"):
                list_item.setBackground(QBrush(QColor("#ADD8E690EE90")))  # Svetlozelena
            elif usb.get("Is active") and not usb.get("Is_registered"):
                list_item.setBackground(QBrush(QColor("#FFFFE0")))  # Svetložuta
            elif usb.get("Is active") and usb.get("Is_registered"):
                list_item.setBackground(QBrush(QColor("#ADD8E6")))  # Svetloplava
            elif not usb.get("Is active") and usb.get("Is_registered"):
                list_item.setBackground(QBrush(QColor("white")))  # Standardna bela
            elif not usb.get("Is active") and not usb.get("Is_registered"):
                list_item.setBackground(QBrush(QColor("#D3D3D3")))  # Svetlo siva
            else:
                list_item.setBackground(QBrush(QColor("white")))  # Bela (default)

            self.usb_list_widget.addItem(list_item)

        # Podesimo visinu liste u zavisnosti od broja stavki
        self.adjust_list_height()
        
    def adjust_list_height(self):
            """
            Prilagođava visinu QListWidget liste na osnovu broja uređaja.
            """
            num_items = self.usb_list_widget.count()
            max_visible_items = 3
            item_height = 30
            if num_items > 0:
                self.usb_list_widget.setVisible(True)
                self.usb_list_widget.setFixedHeight(min(num_items, max_visible_items) * item_height)
            else:
                self.usb_list_widget.setVisible(False)  # Sakrijemo ako nema uređaja
                
    def check_connected_usb_devices(self):
        """
        Proverava trenutno priključene USB uređaje i dodaje ih u listu uređaja.
        """
        print(f" proverava jel ima prikljucenih ")
        try:
            context = pyudev.Context()
            
            for device in context.list_devices(subsystem='block', DEVTYPE='partition'):
                # Proveri da li je USB uređaj
                if 'usb' in device.device_path:
                    device_path = device.device_node  # Npr., '/dev/sdb1'
                    self.main.handle_usb_event("add", device_path)
        except Exception as e:
            print(f"Greška pri proveri priključenih USB uređaja: {e}")

        
    # def closeEvent(self, event):
    #     """Sakrij prozor sa task bara kada se klikne X."""
    #     event.ignore()
    #     self.hide()
        
    # Ovde možete dodati dodatne funkcionalnosti, poput prikazivanja notifikacije u tray-u
        
    # def update_usb_status(self, serial_number , usb):
    #     """Ažurira GUI u zavisnosti od statusa umetnutog USB-a."""
    #     if usb["Is current"]:
    #         self.ui.label.setText(f"USB: { usb['Label']} (Serijski broj: {serial_number})")
    #         self.ui.statusLabel.setText("USB je povezan.")
    #         self.ui.changeButton.setVisible(True)

    #         if usb["Is registar"]:
    #             self.ui.changeButton.setText("Backup")
    #             self.ui.statusLabel.setStyleSheet("color: green;")
    #             self.ui.statusLabel.setText("USB je registrovan. Spreman za backup.")
    #         else:
    #             self.ui.changeButton.setText("Registruj USB")
    #             self.ui.statusLabel.setStyleSheet("color: red;")
    #             self.ui.statusLabel.setText("USB nije registrovan. Registrujte ga.")
    #     else:
    #         self.ui.label.setText("USB nije priključen")
    #         self.ui.statusLabel.setText("")
    #         self.ui.changeButton.setVisible(False)

 
    # def usb_inserted(self, serial_number, usb):
    #     print("usao je u handle") 
    #     print("add")
    #     print(f"u insert usb jee { usb }")
    #     print(f"povrtane inf serijski { serial_number}  i  info  {usb['Label']}")
        
    #     print(f"usb info je : { usb }")
        
    #     self.ui.label.setText(f"USB: { usb['Label'] } Serijski broj: { serial_number }")
    #     self.ui.statusLabel.setText(f"USB je povezan na {usb['Device']}.")
    #     self.ui.changeButton.setVisible(True)
        
        
    
    # def usb_remove(self, serial_number):
    #     # Uklanjanje informacija o USB-u
    #     self.usb_class.usb_info_manager.update_usb_info(serial_number, {"Is current": False})
    #     self.usb_class.usb_info_manager.remove_device(serial_number)
    #     print(f"usb info je : {self.usb_info}")
    #     self.ui.label.setText("USB nije priključen")
    #     self.ui.statusLabel.setText("")
    #     self.ui.changeButton.setVisible(False)
# Pokretanje aplikacije
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow("hjsj")
    window.show()
    app.exec()