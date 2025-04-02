import os
import json
from usb_class import UsbClassManager
from utils.usb_serial import USBSerialManager
from utils.json_file import load_json_data, save_json_data

class BackupFolderManager:
    
    def __init__(self, usb_class):
        self.usb_class = usb_class
        self.deleted_files = []  # Lista obrisanih fajlova, učitana ili nova
        self.backup_path = self.usb_class_manager.json_files.get_backup_path_from_config()
        
    def prepare_backup_folder(self, usb_files):
        """Priprema folder za backup i ažurira listu obrisanih fajlova."""
        
        # Učitaj obrisane fajlove iz prethodnog backup-a
        self.deleted_files = self.load_last_deleted_files()

        # Ažuriraj obrisane fajlove uklanjanjem onih koji su ponovo prisutni na USB-u
        self.deleted_files = self.update_deleted_files(usb_files)

        # Identifikuj nove obrisane fajlove
        for file_path in usb_files:
            if file_path not in self.deleted_files:
                self.deleted_files.append(file_path)

        # Sačuvaj ažuriranu listu obrisanih fajlova u novi `.deleted_files.json`
        deleted_files_path = os.path.join(self.backup_path, ".deleted_files.json")
        save_json_data(deleted_files_path, self.deleted_files, 4)
        USBSerialManager.create_hidden_file(deleted_files_path,self.deleted_files, 4)
        
        print(f"Ažurirana lista obrisanih fajlova sačuvana u: {deleted_files_path}")

    def load_last_deleted_files(self):
        """Učitaj listu obrisanih fajlova iz poslednjeg backupa."""
        
        # Učitaj podatke iz `.serial` fajla ili sličnog JSON-a sa istorijom
        data = load_json_data(self.backup_path)

        # Izvuci putanju poslednjeg backupa iz `backup_history`
        backup_history = data.get("backup_history", [])
        if backup_history:
            last_backup_path = backup_history[-1]  # Poslednji backup folder

            # Proveri da li postoji `.deleted_files.json` u poslednjem backup folderu
            deleted_files_path = os.path.join(last_backup_path, ".deleted_files.json")
            if os.path.exists(deleted_files_path):
                with open(deleted_files_path, 'r') as f:
                    return json.load(f)
            else:
                print(".deleted_files.json ne postoji u poslednjem backup folderu.")
                return []
        return []

    def update_deleted_files(self, usb_files):
        """Ažurira listu obrisanih fajlova uklanjanjem onih koji su ponovo prisutni na USB-u."""
        
        # Kreiramo novu listu sa fajlovima koji nisu prisutni na USB-u
        updated_deleted_files = [file for file in self.deleted_files if file not in usb_files]
        return updated_deleted_files
