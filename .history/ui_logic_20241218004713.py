from ui_gui import Ui_USBBackup
from PySide6.QtWidgets import QListWidgetItem


class UiLogic:
    def __init__(self, main_window):
        self.ui_usb_backup = Ui_USBBackup()
        self.ui_usb_backup.setupUi(main_window)
        self.main_window = main_window
        
    def toggle_left_widget(self, bool):
        """Prikaz/Sakrivanje levog dela."""
        self.ui_usb_backup.left_widget.setVisible( bool)
        self.ui_usb_backup.adjust_window_size()

    def toggle_right_widget(self, bool):
        """Prikaz/Sakrivanje desnog dela."""
        self.ui_usb_backup.right_widget.setVisible(bool)
        self.ui_usb_backup.adjust_window_size()

    def adjust_window_size(self):
        """Prilagođavanje širine i centriranje prozora."""
        # Početna širina središnjeg dela
        width = 200  # Širina središnjeg dela bez dodataka
        # Dodaj širinu za vidljive delove
        if self.ui_usb_backup.left_widget.isVisible():
            width += 155  # Širina levog dela
        if self.ui_usb_backup.right_widget.isVisible():
            width += 222  # Širina desnog dela

        # Postavi novu veličinu prozora
        current_geometry = self.ui_usb_backup.MainWindow.geometry()
        print(f" nova geeometrija .....{ current_geometry } i  .... { width}")
        self.ui_usb_backup.MainWindow.setFixedSize(width, current_geometry.height())
            
    def update_backup_list(self, backups):
        """Ažurira listu backup-ova u levom widget-u."""
        self.ui_usb_backup.backup_list.clear()  # Briše prethodni sadržaj
        print("usao u list backup")        
        self.ui_usb_backup.toggle_left_widget(True)
        print(f"levo krilo je ......{self.left_widget.isVisible()}")
        for backup in backups:
            item = QListWidgetItem(backup)  # Kreira novi element za svaki backup
            self.ui_usb_backup.backup_list.addItem(item)
                        
    def usb_inserted(self, serial_number, usb):
        print("usao je u ui instert") 
        print(f"povrtane inf serijski { serial_number}  i  info  {usb['Label']}")
        if serial_number:
            self.ui_usb_backup.label.setText(f"USB: { usb['Label'] } Serijski broj: { serial_number }")
            self.ui_usb_backup.statusLabel.setText(f"USB je povezan na {usb['Device']}.")
            self.ui_usb_backup.changeButton.setVisible(True)
        else:
            self.ui_usb_backup.label.setText(f"USB nije umetnut")
            self.ui_usb_backup.statusLabel.setText(f"")
            self.ui_usb_backup.changeButton.setVisible(False)
        
    def usb_remove(self, serial_number):
        # Uklanjanje informacija o USB-u
        self.ui_usb_backup.label.setText("USB nije priključen")
        self.ui_usb_backup.statusLabel.setText("")
        self.ui_usb_backup.backup_list.clear()
        
        self.ui_usb_backup.toggle_left_widget(False)
        print(f"levo krilo je ......{self.ui_usb_backup.left_widget.isVisible()}")
        print(f"desno krilo je ......{self.ui_usb_backup.right_widget.isVisible()}")
        
                    
    def update_usb_status(self, serial_number , usb):
        """Ažurira GUI u zavisnosti od statusa umetnutog USB-a."""
        if usb["Is current"]:
            self.ui_usb_backup.label.setText(f"USB: { usb['Label']} (Serijski broj: {serial_number})")
            self.ui_usb_backup.statusLabel.setText("USB je povezan.")
            self.ui_usb_backup.changeButton.setVisible(True)

            if usb["Is registar"]:
                self.ui_usb_backup.changeButton.setText("Backup")
                self.ui_usb_backup.statusLabel.setStyleSheet("color: green;")
                self.ui_usb_backup.statusLabel.setText("USB je registrovan. Spreman za backup.")
            else:
                self.ui_usb_backup.changeButton.setText("Registruj USB")
                self.ui_usb_backup.statusLabel.setStyleSheet("color: red;")
                self.ui_usb_backup.statusLabel.setText("USB nije registrovan. Registrujte ga.")
        else:
            self.ui_usb_backup.label.setText("USB nije priključen")
            self.ui_usb_backup.statusLabel.setText("")
            self.ui_usb_backup.changeButton.setVisible(False)
        
    # def closeEvent(self, event):
    #     """Sakrij prozor sa task bara kada se klikne X."""
    #     event.ignore()
    #     self.hide()
    
   