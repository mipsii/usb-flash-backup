from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import QListWidgetItem

class UsbInfoManager:
    """Rukuje informacijama o uređajima, kao što su ažuriranje i pretraga informacija."""
    def __init__(self ):
                
        self.usb_info = {}
        
    def get_current_usb_info(self):
        """Vraća informacije o trenutnom uređaju za prikaz u GUI-ju."""
        for sserial_number, details in self.usb_info.items():
            if details.get('Is current'):  # Proverava postojanje ključa i njegovu vrednost
                return sserial_number, details
        return None  # Ako nijedan uređaj nije označen kao 'Is current'

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
        #self.update_usb_info(serial_number, {"Is register": False})
        # for serial, usb in self.usb_info.items():
        #     if serial == serial_number:
        #         usb['Active'] = False
        #         print(f"USB uređaj sa serijskim brojem {serial} je deaktiviran.")
        #         break
                  
    def update_current_usb(self, serial_number=None):
        """Ažurira trenuni prikazani uređaj."""  
         # Postavi trenutni uređaj ako je serijski broj prisutan
        if serial_number and serial_number in self.usb_info:
            self.usb_info[serial_number]["Is current"] = True
            print(f"Ažuriran uređaj: {self.usb_info[serial_number]["Label"]} kao trenutni.")
        else:
            print("Nema aktivnog uređaja.")
       
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
        
    def update_usb_list(self, usb_list_widget):
        """
        Ažurira QListWidget listu sa USB uređajima, sa odgovarajućim bojama za status.
        """
        usb_list_widget.clear()  # Obrisati sve stavke pre ažuriranja
        
        for serial_usb, usb in self.usb_info.items():     
            item_text = f"{ usb['Label'] }"
            list_item = QListWidgetItem(item_text)  # Kreiranje QListWidgetItem sa tekstom
          
            # Čuvaj serijski broj u stavci da bi ga koristio kasnije
            list_item.setData(0, serial_usb)
            
             # Postavljamo boju pozadine na osnovu statusa
            if usb['Is current']:
                list_item.setBackground(QBrush(QColor("#ADD8E6")))  # Svetloplava
            elif not usb['Is registar']:
                list_item.setBackground(QBrush(QColor("#FFFFE0")))  # Svetložuta
            else:
                list_item.setBackground(QBrush(QColor("white")))  # Standardna boja

            usb_list_widget.addItem(list_item)
            
        usb_list_widget = self.adjust_list_height(usb_list_widget)
        return usb_list_widget     
    