import asyncio
import sys
import time
from PySide6.QtWidgets import QMainWindow, QApplication
import pyudev
from PySide6.QtGui import Qt
from file_change import FileChangeManager
from PySide6.QtCore import Signal

from ui_gui import UiGui
from ui_logic import UiLogic

class MainWindow(QMainWindow):
    analyze_files = Signal()
    def __init__(self, usb_class):
        super().__init__()
        self.usb_class = usb_class
             
        # Inicijalizacija korisničkog interfejsa
        self.ui_gui = UiGui()
        self.ui_gui.setupUi(self)
        self.ui_logic = UiLogic(self)
        #self.check_connected_usb_devices()
        print("u main u je ")
              
    def _initiate(self):
        self.file_change.history_changed.connect(self.ui_logic.update_backup_list)          
        self.analyze_files.connect(lambda: asyncio.create_task(self.file_change.analyze_changes()))
    def add_usb(self):
        print("Dodavanje USB uređaja.")
        # Implementirajte funkcionalnost za ažuriranje stanja USB uređaja

    def handle_usb_event(self, action, deviceID):
        """Rukuje događajem umetanja ili uklanjanja USB-a."""
        print(f"promena sa  usb ..... {action} ..... { deviceID}")
        if action == "add":
            device = self.usb_class.usb_device.get_connected_usb_devices(deviceID)
            # Preuzimanje informacija o uređaju na osnovu serijskog broja
            serial_number = device["Serial number"]
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
            if mount:
                self.usb_class.add_usb_info(serial_number, device.get(("Label")), deviceID, 
                                        mount, 
                                        register_bool = True, current_bool = True, active_bool = True)
                self.usb_class.update_current_usb(serial_number)
                self.ui_gui.usb_inserted(serial_number, self.usb_class.usb_info[serial_number])
            
                try:
                    #loop = asyncio.get_running_loop()
                    asyncio.create_task(self.analyz_files(mount, serial_number))
                except RuntimeError as e:
                    print(f"Greška: asyncio petlja nije aktivna - {e}")
            else:
                print("opet nije ....")

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
                self.ui_gui.usb_remove(serial_number)
            else:
                print("laznjak")

        if device:    
            #self.ui.update_usb_status(serial_number, self.usb_class.usb_info[serial_number])
            self.ui_logic.add_usb()
            pass
   
    async def analyz_files(self,usb_backup, sserial_number):
        print("usao je u ......-------analyz_file")
        backup_path = self.usb_class.usb_folder.find_usb_folder(sserial_number)
        self.file_change = FileChangeManager( backup_path, usb_backup )
        print(f"kreiran file_change")
        self._initiate()
        self.analyze_files.emit()
        #await self.file_change.analyze_changes()
        
    def ss(self, history):
        print(f"stigao je spisak .....{ history }")
        

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
                    self.handle_usb_event("add", device_path)
        except Exception as e:
            print(f"Greška pri proveri priključenih USB uređaja: {e}")

        
    # def closeEvent(self, event):
    #     """Sakrij prozor sa task bara kada se klikne X."""
    #     event.ignore()
    #     self.hide()
        
    # Ovde možete dodati dodatne funkcionalnosti, poput prikazivanja notifikacije u tray-u
   
# Pokretanje aplikacije
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow("hjsj")
    window.show()
    app.exec()