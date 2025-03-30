class UsbBackupUi:
    
    def toggle_left_widget(self, bool):
        """Prikaz/Sakrivanje levog dela."""
        self.left_widget.setVisible( bool)
        self.adjust_window_size()

    def toggle_right_widget(self, bool):
        """Prikaz/Sakrivanje desnog dela."""
        self.right_widget.setVisible(bool)
        self.adjust_window_size()

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
        current_geometry = self.MainWindow.geometry()
        print(f" nova geeometrija .....{ current_geometry } i  .... { width}")
        self.MainWindow.setFixedSize(width, current_geometry.height())
            
    def update_backup_list(self, backups):
        """Ažurira listu backup-ova u levom widget-u."""
        self.backup_list.clear()  # Briše prethodni sadržaj
        print("usao u list backup")        
        self.toggle_left_widget(True)
        print(f"levo krilo je ......{self.left_widget.isVisible()}")
        for backup in backups:
            item = QListWidgetItem(backup)  # Kreira novi element za svaki backup
            self.backup_list.addItem(item)
                        
    def usb_inserted(self, serial_number, usb):
        print("usao je u ui instert") 
        print(f"povrtane inf serijski { serial_number}  i  info  {usb['Label']}")
        if serial_number:
            self.label.setText(f"USB: { usb['Label'] } Serijski broj: { serial_number }")
            self.statusLabel.setText(f"USB je povezan na {usb['Device']}.")
            self.changeButton.setVisible(True)
        else:
            self.label.setText(f"USB nije umetnut")
            self.statusLabel.setText(f"")
            self.changeButton.setVisible(False)
        
    def usb_remove(self, serial_number):
        # Uklanjanje informacija o USB-u
        self.label.setText("USB nije priključen")
        self.statusLabel.setText("")
        self.backup_list.clear()
        
        self.toggle_left_widget(False)
        print(f"levo krilo je ......{self.left_widget.isVisible()}")
        print(f"desno krilo je ......{self.right_widget.isVisible()}")
        
                    
    def update_usb_status(self, serial_number , usb):
        """Ažurira GUI u zavisnosti od statusa umetnutog USB-a."""
        if usb["Is current"]:
            self.label.setText(f"USB: { usb['Label']} (Serijski broj: {serial_number})")
            self.statusLabel.setText("USB je povezan.")
            self.changeButton.setVisible(True)

            if usb["Is registar"]:
                self.changeButton.setText("Backup")
                self.statusLabel.setStyleSheet("color: green;")
                self.statusLabel.setText("USB je registrovan. Spreman za backup.")
            else:
                self.changeButton.setText("Registruj USB")
                self.statusLabel.setStyleSheet("color: red;")
                self.statusLabel.setText("USB nije registrovan. Registrujte ga.")
        else:
            self.label.setText("USB nije priključen")
            self.statusLabel.setText("")
            self.changeButton.setVisible(False)
        
    # def closeEvent(self, event):
    #     """Sakrij prozor sa task bara kada se klikne X."""
    #     event.ignore()
    #     self.hide()
    
   