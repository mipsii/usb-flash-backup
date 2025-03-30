import asyncio
from PySide6.QtCore import  QObject
from PySide6.QtGui import  Qt
from usb_list import USBListManager
from PySide6.QtCore import Signal

class UiLogic(QObject):
    upddate_gui = Signal(str)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.usb_class = self.main_window.usb_class
        self.ui = self.main_window.ui_gui
        self.managerList = USBListManager( self.main_window, self.main_window.usb_class)
        self.ui.usbList = self.managerList.usb_list_widget  # Pravilno dodeljivanje usb_list_widget
        self.ui.vertical_layout.addWidget(self.ui.usbList)
        # Povezujemo dugme sa akcijom
        self.selected_item = None  # Čuvamo selektovani item
        self._initiate()

    def _initiate(self):
        self.ui.changeButton.clicked.connect(self.on_change_button_clicked)
        #self.upddate_gui.connect(self.main_window.analyz_files)
        self.upddate_gui.connect(lambda: asyncio.create_task(self.main_window.analyz_files(serial)))
        
    def on_change_button_clicked(self):
        if self.ui.changeButton.text() == "Backup":
            self.ui.set_status_message("Pokrenut backup...", "green")
            asyncio.create_task(self.main_window.file_change.gg())
        else:
            self.ui.set_status_message("Registracija USB-a...", "red")
            serial_number, details = self.main_window.usb_class.usb_info_manager.get_current_usb_info()
            label = details["Label"]
            self.main_window.usb_class.usb_folder.create_hidden_file_with_serial_number(label, serial_number)
            self.main_window.usb_class.usb_info_manager.update_usb_info(serial_number, {"Is registar": True})
            
    def update_backup_list(self, backups):
        """Logika za ažuriranje liste backup-ova."""
        self.ui.update_backup_list_widget(backups)  # Ažurira sadržaj liste u interfejsu
        self.ui.toggle_left_widget(True)  # Prikazuje levi widget
        print(f"Levo krilo je ......{self.ui.left_widget.isVisible()}")

    def add_usb(self):
        """Dodaje USB uređaj u listu."""
        self.managerList.update_usb_list()
        # Ako veza nije već postavljena, postavi signal
        if not hasattr(self, "_item_clicked_connected") or not self._item_clicked_connected:
            self.ui.usbList.itemClicked.connect(self.on_item_clicked)
            self._item_clicked_connected = True       

    def on_item_clicked(self, item):
        serial_number = item.data(Qt.UserRole)  # Preuzima serijski broj iz stavke
        if self.selected_item == item:
            self.selected_item = None
            self.ui.usbList.clearSelection()
            self.ui.usb_remove(serial_number)
        else:    
            """Obradjuje klik na stavku u listi."""
            print(f" serijski broj u lsiti je ....{serial_number}")
            self.selected_item = item
            # Koristi metodu find_device da pronađeš podatke o USB uređaju
            serial, usb_data = self.usb_class.usb_device.find_device(serial_number=serial_number)
            usb_data["Is current"] = True

            self.upddate_gui.emit(serial)
            print(f"Signal emitovan sa: {serial}")
            self.main_window.signal_gui(serial)
                
    def usb_status_to_add_usb_wrapper(self, serial_number, usb_info):
        self.add_usb()
    
    
    # def closeEvent(self, event):
    #     """Sakrij prozor sa task bara kada se klikne X."""
    #     event.ignore()
    #     self.hide()
    
   