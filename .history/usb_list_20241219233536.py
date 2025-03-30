from PySide6.QtGui import QColor, QBrush, Qt
from PySide6.QtWidgets import QListWidgetItem, QListWidget

class USBListManager:
    def __init__(self, parent_layout, usb_class):
        """
        Inicijalizuje USBListManager sa QListWidget objektom za prikaz USB uređaja.
        """
         # Glavni prozor
        self.usb_class = usb_class  # Instanca USBClass za podatke o USB uređajima
        # Kreiramo QListWidget za prikaz USB uređaja
        self.usb_list_widget = QListWidget(parent_layout)
        self.usb_list_widget.setStyleSheet("font-family: 'Courier New'; font-size: 14px;")
        self.usb_list_widget.setFixedHeight(15)  # Ograničavamo visinu
        self.usb_list_widget.setVisible(False)  # Početno sakriveno

        #self.update_usb_list()
   
    def usb_list(self):
        for  device_id, usb in self.usb_info.items():
            is_current = True
            is_registered = True 
            self.add_device_info(device_id, usb['Label'],is_current, is_registered )

    def update_usb_list(self):
        """
        Ažurira QListWidget listu sa USB uređajima, sa odgovarajućim bojama za status.
        """
        self.usb_list_widget.clear()  # Obrisati sve stavke pre ažuriranja

        for serial_number, usb in self.usb_class.usb_info.items():
            print(f" ucitavanje lsit  {usb.get('Label')}")
            item_text = f"{usb.get('Label')} - "
            print(f"item text {item_text}")
            list_item = QListWidgetItem(item_text)
            
            # Čuvaj serijski broj u stavci da bi ga koristio kasnije
            list_item.setData(Qt.UserRole, serial_number)
            
            if not usb["Active"]:  # Proverite da li je USB aktivan
                list_item.setFlags(list_item.flags() & ~Qt.ItemIsEnabled)  # Onemogućite stavku
            # Dodavanje boje pozadine na osnovu statusa
            if usb.get('Is current'):
                # Trenutni uređaj
                list_item.setBackground(QBrush(QColor("#ADD8E690EE90")))  # Svetlozelena
                
            elif usb.get('Active') and not usb.get('Is registar'):
                # Aktivni, neregistrovani uređaj
                list_item.setBackground(QBrush(QColor("#FFFFE0")))  # Svetložuta
                
            elif usb.get('Active') and usb.get('Is registar'):
                # Aktivni, registrovani uređaj
                list_item.setBackground(QBrush(QColor("#ADD8E6")))  # Svetloplava
                
            elif not usb.get('Active') and usb.get('Is registar'):
                # Neaktivni, ali registrovani uređaj
                list_item.setBackground(QBrush(QColor("white")))  # Standardna bela
                
            elif not usb.get('Active') and not usb.get('Is registar'):
                # Neaktivni i neregistrovani uređaj
                list_item.setBackground(QBrush(QColor("#D3D3D3")))  # Svetlo siva
            else:
                # Ostala stanja (default)
                list_item.setBackground(QBrush(QColor("white")))  # Bela
                    
            #self.usb_list_widget.addItem(list_item)
            
            self.usb_list_widget.addItem(list_item)
        # Podesimo visinu liste u zavisnosti od broja stavki
        self.adjust_list_height()

    def adjust_list_height(self):
        """
        Prilagođava visinu QListWidget liste na osnovu broja uređaja.
        """
        num_items = self.usb_list_widget.count()
        max_visible_items = 3
        item_height = 20
        if num_items > 0:
            self.usb_list_widget.setVisible(True)
            self.usb_list_widget.setFixedHeight(min(num_items, max_visible_items) * item_height)
        else:
            self.usb_list_widget.setVisible(False)  # Sakrijemo ako nema uređaja
