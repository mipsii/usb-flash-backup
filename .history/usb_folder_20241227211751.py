import os
import platform
import shutil
from datetime import datetime

class USBFolderManager:
    def __init__(self, usb_class):
        self.usb_class = usb_class
        
        self.backup_base_path = self.get_backup_base_path()
        self.usb_folder_path = None
        self.serial_file_path = None

    def get_backup_base_path(self):
        return self.usb_class.json_files.get_backup_path_from_config()
    
    def find_usb_folder(self, serial_number):
        """Proverava da li postoji folder za USB uređaj sa zadatim serijskim brojem."""
        print(f"putanaja  je { self.backup_base_path}")
        if not os.path.isdir(self.backup_base_path):
            return None
        
        #serial_number = self.usb_class.get_serial_number(device)
        for folder_name in os.listdir(self.backup_base_path):
            folder_path = os.path.join(self.backup_base_path, folder_name)
            if os.path.isdir(folder_path):
                hidden_file_path = os.path.join(folder_path, ".serial")
                if os.path.exists(hidden_file_path):
                    data = self.usb_class.json_files.load_json_data(hidden_file_path)
                    if data.get("serial_number") == serial_number:
                        print("Postoji folder za ovaj serijski broj.")
                        #self.add_register_path_seial(device, folder_path)
                        return folder_path
                    else:
                        print("Serijski broj se ne poklapa.")
            else:
                print("Skriveni fajl ne postoji.")
        return None

    def create_usb_folder(self, usb_label, serial_number):
        """Kreira folder za USB uređaj i dodaje skriveni fajl sa serijskim brojem i osnovnim informacijama."""
        backup_folder = self.usb_class.json_files.get_backup_path_from_config()
         # Kreiraj putanju za USB uređaj
        usb_folder_path = os.path.join(backup_folder, usb_label)

        # Proveri da li folder postoji
        if not os.path.exists(usb_folder_path):
            print(f"Kreiranje foldera: {usb_folder_path}")
            os.makedirs(usb_folder_path)
        else:
            print(f"Folder već postoji: {usb_folder_path}")
            
        data = {
            "serial_number": serial_number,
            "label": usb_label,
            "created_at": datetime.now().isoformat(),
            "backup_history": []
        }
        self._create_hidden_file(data, usb_folder_path)
        print(f"Kreiran je folder za USB: {self.usb_folder_path}")

    def _create_hidden_file(self, data, usb_folder_path):
        """Kreira skriveni fajl sa serijskim brojem i dodatnim informacijama."""
        serial_file_path =os.path.join(usb_folder_path, ".serial")

        self.usb_class.json_files.save_json_data(serial_file_path, data)
        
        if platform.system() == "Windows":
            os.system(f'attrib +h "{self.serial_file_path}"')
        print(f"Skriveni fajl kreiran: {self.serial_file_path}")

    def update_backup_history(self, new_backup_path):
        """Ažurira istoriju backup-ova i čuva samo poslednjih 8 unosa."""
        data = self.load_json_data(self.serial_file_path)
        if not data:
            data = {"backup_history": []}

        backup_history = data.get("backup_history", [])
        backup_history.append({"path": new_backup_path, "date": datetime.now().isoformat()})

        if len(backup_history) > 8:
            self.delete_backup_folder(backup_history[1]["path"])
            backup_history.pop(1)

        data["backup_history"] = backup_history
        self.save_json_data(self.serial_file_path, data)

    def update_backup_history(self, new_backup_path, deleted_files):
        """ Ažurira istoriju backup-a i dodaje obrisane fajlove u odgovarajući backup folder."""
        # Učitaj podatke iz .serial fajla
        data = self.load_json_data(self.serial_file_path) or {
            "serial_number": self.usb_class.serial_number,
            "name": self.usb_class.name,
            "created_at": datetime.now().isoformat(),
            "backup_history": []
        }

        # Snimi obrisane fajlove u trenutni backup folder
        deleted_files_path = os.path.join(new_backup_path, "deleted_files.json")
        self.save_json_data(deleted_files_path, deleted_files)

        # Dodaj novi backup u istoriju
        data["backup_history"].append({
            "path": new_backup_path,
            "date": datetime.now().isoformat()
        })

        # Ograniči broj backup-ova na 8
        if len(data["backup_history"]) > 8:
            oldest_backup = data["backup_history"].pop(1)
            self.delete_backup_folder(oldest_backup["path"])

        # Snimi ažurirani .serial fajl
        self.save_json_data(self.serial_file_path, data)

    def delete_backup_folder(self, folder_path):
        """Briše dati folder i njegov sadržaj."""
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
            print(f"Obrisan folder: {folder_path}")

    def add_register_path_seial(self, device, folder_path):
        self.usb_info[device].update({
            'is_registered': True,
            'serial_file_path': folder_path
        })
       
    