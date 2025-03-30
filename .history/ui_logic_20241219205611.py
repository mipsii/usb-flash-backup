import asyncio
from ui_gui import UiGui
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import  QObject

from usb_list import USBListManager

class UiLogic(QObject):
    def __init__(self, main_window):
        self.main_window = main_window
        self.usb_class = self.main_window.usb_class
        self.ui = self.main_window.ui_gui
        self.managerList = USBListManager( self.main_window, self.main_window.usb_class)
        self.ui.usbList = self.managerList.usb_list_widget  # Pravilno dodeljivanje usb_list_widget
        self.ui.vertical_layout.addWidget(self.ui.usbList)
        # Povezujemo dugme sa akcijom
        self._initiate()

    def _initiate(self):
        self.ui.changeButton.clicked.connect(self.on_change_button_clicked)
        pass
    
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
        """Ažurira listu backup-ova u levom widget-u."""
        self.ui.backup_list.clear()  # Briše prethodni sadržaj
        print("usao u list backup")        
        self.ui.toggle_left_widget(True)
        print(f"levo krilo je ......{self.ui.left_widget.isVisible()}")
        for backup in backups:
            item = QListWidgetItem(backup)  # Kreira novi element za svaki backup
            self.ui.backup_list.addItem(item)

    def add_usb(self):
        """Dodaje USB uređaj u listu."""
        self.managerList.update_usb_list()
        # Ako veza nije već postavljena, postavi signal
        if not hasattr(self, "_item_clicked_connected") or not self._item_clicked_connected:
            #self.ui.usbList.itemClicked.connect(self.on_item_clicked)
            self._item_clicked_connected = True       
                    
    def update_usb_status(self, serial_number , usb):
        """Ažurira GUI u zavisnosti od statusa umetnutog USB-a."""
        if usb["Is current"]:
            self.ui.label.setText(f"USB: { usb['Label']} (Serijski broj: {serial_number})")
            self.ui.statusLabel.setText("USB je povezan.")
            self.ui.changeButton.setVisible(True)

            if usb["Is registar"]:
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
    
    def adjust_window_size(self):
        """Prilagođavanje širine i centriranje prozora."""
        # Početna širina središnjeg dela
        width = 200  # Širina središnjeg dela bez dodataka
        # Dodaj širinu za vidljive delove
        if self.left_widget.isVisible():
            width += 155  # Širina levog dela
        if self.right_widget.isVisible():
            width += 222  # Širina desnog dela

        # Postavi novu veličinu prozora
        current_geometry = self.main_window.geometry()
        print(f" nova geeometrija .....{ current_geometry } i  .... { width}")
        self.main_window.setFixedSize(width, current_geometry.height())
    # def closeEvent(self, event):
    #     """Sakrij prozor sa task bara kada se klikne X."""
    #     event.ignore()
    #     self.hide()
    
   