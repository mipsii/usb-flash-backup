from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QListWidgetItem

from src.signals.signal_manager import SignalManager

class UsbInfoManager:
    """Rukuje informacijama o uređajima, kao što su ažuriranje i pretraga informacija."""
    def __init__(self ):
                
        self.usb_info = {}
        
    def _signal(self):
        self.signal_manager = SignalManager()
        self.signal_manager.connect_signal("sigRemoveUsb", self, "remove_device")
        self.signal_manager.connect_signal("sigRemoveUsb", self, "test")
    def get_current_usb_info(self):
        """Vraća informacije o trenutnom uređaju za prikaz u GUI-ju."""
        for sserial_number, details in self.usb_info.items():
            if details.get('Is current'):  # Proverava postojanje ključa i njegovu vrednost
                return sserial_number, details
        return None  # Ako nijedan uređaj nije označen kao 'Is current'

    def test(self, serial):
        print(f"...primeio je sa signala usbremoveusb je ...{serial}")
    def get_usb_info(self):
        return self.usb_info
    
    def get_atribut_usb(self, serial_number):
        if serial_number in self.usb_info:
            return self.usb_info[serial_number]
        else:
            #raise ValueError(f"USB sa serijskim brojem {serial_number} nije pronađen.")
            return False
            
    def get_serial_number(self, device):
        for serial, info in self.usb_info.items():
            if info["Device"] == device:
                return serial
              
    def remove_device(self, serial_number):
        """Uklanja uređaj iz usb_info kada se ukloni sa sistema."""

        self.update_usb_info(serial_number, {"Is current": False})
        self.update_usb_info(serial_number, {"Active": False})
        self.update_usb_info(serial_number, {"Device": ""})
        self.update_usb_info(serial_number, {"Mount Point": ""})
        print("--------nulovanje info usb -------")
        self.signal_manager.emit_signal("sigUsbStatusChanged", self.usb_info[serial_number])
                  
    def update_current_usb(self, serial_number=None):
        """Ažurira trenuni prikazani uređaj."""  
         # Postavi trenutni uređaj ako je serijski broj prisutan
        if serial_number and serial_number in self.usb_info:
            self.usb_info[serial_number]["Is current"] = True
            print(f"Ažuriran uređaj: {self.usb_info[serial_number]["Label"]} kao trenutni.")
        else:
            print("Nema aktivnog uređaja.")
            self.usb_info[serial_number]["Is current"] = False
       
    def add_usb_info(self, serial_number, label, device, mount_point, register_bool = False, current_bool = False, active_bool = False):
        """Dodaje USB uređaj u listu informacija."""
        print("Dodavanje USB uređaja u recnik.")
        self.usb_info[serial_number] = {
            'Label': label,
            'Device': device,
            'Mount Point': mount_point,
            'Is registar': register_bool,
            'Is current': current_bool,
            'Active': active_bool
        }
        print("Dodati elementi:")
        for key, value in self.usb_info.items():
            print("----------------------------------")
            print(f"{key}: {value}")
            print("----------------------------------")
    
    def update_usb_info(self, serial_number, updates):
        self.usb_info[serial_number].update(updates)
        print(f"USB {serial_number} ažuriran: {updates}")
   