import asyncio

from datetime import datetime
from PySide6.QtCore import  QObject
from PySide6.QtGui import  Qt
from signal_manager import SignalManager
from usb_list import USBListManager
from PySide6.QtCore import Signal

class UiLogic(QObject):
    upddate_gui = Signal(str)
    signal_gui = Signal(str, dict)
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
        
        self._signals()
        
    def _signals(self):
        self.signal_manager = SignalManager()
        self.signal_manager.connect_signal("usb_status_changed", self, "usb_status_to_add_usb_wrapper")
        self.signal_manager.connect_signal("history_changed", self, "update_backup_list")

    def _initiate(self):
        self.ui.changeButton.clicked.connect(self.on_change_button_clicked)
        #self.upddate_gui.connect(self.main_window.analyz_files)
        self.upddate_gui.connect(lambda serial: asyncio.create_task(self.main_window.analyz_files(serial)))
        self.signal_gui.connect(self.ui.update_usb_status)
        self.ui.backup_list.itemClicked.connect(self.on_backup_clicked)
        
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
        print(f"iz logic update_backup_list ... history je ....{backups}")
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
        if not item:
            return  # Proverava da li je validan klik

        serial_number = item.data(Qt.UserRole)  # Preuzima serijski broj iz stavke

        # Ako je stavka već selektovana, poništi selekciju
        if self.selected_item == serial_number:
            self.selected_item = None
            print(f"USB sa serijskim brojem {serial_number} je deaktiviran.")
            self.ui.usb_remove(serial_number)  # Ažurira GUI za deaktivaciju
            return

        # Aktivira novu selekciju
        self.selected_item = serial_number
        print(f"Serijski broj u listi je: {serial_number}")

        # Pronalazi podatke o USB uređaju
        serial, usb_data = self.usb_class.usb_device.find_device(serial_number=serial_number)
        if usb_data:
            usb_data["Is current"] = True  # Obeležava USB kao aktivan

        # Emituje signal za ažuriranje GUI-ja
        self.upddate_gui.emit(serial)
        print(f"Signal emitovan sa: {serial}")
        print(f" data jew .... { usb_data }")
        # Poziva direktno ažuriranje GUI komponente
        self.signal_gui.emit(serial_number, usb_data)
        #self.main_window.signal_gui(serial, usb_data)
                
    def usb_status_to_add_usb_wrapper(self, serial_number, usb_info):
        self.add_usb()
    
    
    # def closeEvent(self, event):
    #     """Sakrij prozor sa task bara kada se klikne X."""
    #     event.ignore()
    #     self.hide()
    
        
    def format_backup_datetime(self, date_str):
        """Formatira datum u lepi i razumljiviji format."""
        try:
            # Razdvajanje imena fajla na datum i vreme
            parts = date_str.split('_')
            date_str = parts[1]  # 20241214
            time_str = parts[2]  # 000237

            # Pretvaranje datuma i vremena u odgovarajući format
            date_obj = datetime.strptime(date_str, "%Y%m%d")
            time_obj = datetime.strptime(time_str, "%H%M%S")

            # Formatiranje u željeni oblik
            formatted_date = date_obj.strftime("%d.%m.%Y.")
            formatted_time = time_obj.strftime("%H:%M")

            # Spajanje formata u jedan string
            return formatted_date + " " + formatted_time
        except ValueError:
            return date_str  # Ako nešto pođe po zlu, vrati originalni naziv fajl

    def on_backup_clicked(self, item):
        backup_index = item.data(Qt.UserRole)
        backup_path = item.data(Qt.UserRole+1)
        print(f"Kliknut backup: {item.text()} (indeks: {backup_index})")
        merged_state = self.main_window.backup_files_index(backup_path ,backup_index)
        #merged_state = self.main_window.backup_files_index(self.main_windows.ui_logic.history, backup_index)
        print(f"backup po indexu { backup_index} je ...{merged_state} ")
