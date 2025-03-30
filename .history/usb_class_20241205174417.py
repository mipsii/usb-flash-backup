import asyncio
from operator import truediv
import os
import sys
from PySide6.QtWidgets  import QApplication
import pyudev
from qasync import QEventLoop

from json_file import JsonFileManager
from usb_backup_manager import USBBackupManager
from usb_info import UsbInfoManager
from main import MainWindow
from usb_device import USBDeviceManager
from usb_folder import USBFolderManager
from usb_listener import UsbListener

class UsbClassManager:
   
    def __init__(self):
                
        self.inicijalizacije()
        
        print("staruje slusanje")
        # Povezivanje signala
        
        self.load_registered_usb()
        #self.check_connected_usb_devices()
        self.usb_listener.usb_event.connect(self.main.handle_usb_event)
        # Pokretanje slušanja
    
    def __getattr__(self, name):
        # Ako nije pronađeno u trenutnoj klasi, traži u usb_info_manager
        if hasattr(self.usb_info_manager, name):
            return getattr(self.usb_info_manager, name)
        raise AttributeError(f"'UsbClassManager' nema atribut '{name}'")

    def inicijalizacije(self):
        self.main = MainWindow(self)
        self.usb_info_manager = UsbInfoManager()
        self.json_files =  JsonFileManager()
        self.usb_listener = UsbListener(self)
       
        self.usb_folder = USBFolderManager(self)
        
        self.usb_device = USBDeviceManager(self)
        self.usb_backup_manager = USBBackupManager(self)

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
                    # Dobijanje podataka o uređaju
                    # usb_info = self.usb_device.get_connected_usb_devices(device_path)
                    # if usb_info:
                    #     print(f"Pronađen USB uređaj: {usb_info}")
                    #     # Dodaj USB u tvoju internu strukturu
                    #     self.add_device_info(
                    #         device_path=usb_info['Device'], 
                    #         mount_point=usb_info['Mount Point'],
                    #         label=usb_info['Label'],
                    #         serial_number=usb_info['Serial number'],
                    #         register_bool = True,
                    #         current_bool = True,
                    #         active_bool = True)
        except Exception as e:
            print(f"Greška pri proveri priključenih USB uređaja: {e}")


    def load_registered_usb(self):
        """Učitava sve registrovane USB uređaje iz foldera."""
        print("Usao u učitavanje USB uređaja.")
        backup_base_path = self.json_files.get_backup_path_from_config()
        print(backup_base_path)
        if not os.path.exists(backup_base_path):
            print("Direktorijum za backup ne postoji.")
            return

        for folder_name in os.listdir(backup_base_path):
            folder_path = os.path.join(backup_base_path, folder_name)
            hidden_file_path = os.path.join(folder_path, ".serial")

            if os.path.isdir(folder_path) and os.path.exists(hidden_file_path):
                usb_data = self.json_files.load_json_data(hidden_file_path)
                serial_number = usb_data.get("serial_number")
                print(f" serrijski broj je  : { serial_number }")
                label = usb_data.get('label')
                print(f" Label je  : { label }")
                if serial_number:
                    # Dodavanje u usb_info preko metode add_usb_info
                    self.usb_info_manager.add_usb_info(
                        serial_number,
                        usb_data.get("label"),
                        None,  # Ako imate podatke o uređaju, dodajte ih
                        None,  # Ako imate podatke o tački montaže, dodajte ih
                        register_bool=True  # Ako je USB registrovan, postavite True
                    )
                    print(f"Registrovan USB: {serial_number}, ime: {usb_data.get('label')}")
                    
                else:
                    print(f"Neispravan .serial fajl u {folder_path}")
        self.main.add_usb()
        print(f"Ukupno učitano registrovanih USB uređaja: {len(self.usb_info_manager.usb_info)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Kreiramo PyQt event loop i postavljamo ga kao asyncio event loop
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    with loop:
       
        
        try:
            # Kreiranje centralne klase
            usb_manager = UsbClassManager()
            print("kreiran manager")
            # Simulacija detekcije USB-a
            usb_manager.usb_listener.start()
            loop.call_soon(usb_manager.check_connected_usb_devices)
            # Prikaz glavnog prozora
            usb_manager.main.show()
            
        except Exception as e:
            print(f"Greška pri kreiranju manager-a: {e}")
            sys.exit(1)
        loop.run_forever()
    
    sys.exit(app.exec())
