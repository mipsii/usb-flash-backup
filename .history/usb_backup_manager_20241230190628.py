import asyncio
from datetime import datetime
import json
import os
import shutil
from localization import _

class USBBackupManager:
    def __init__(self, file_change_manager):
        """
        Inicijalizuje USBBackupManager sa referencom na FileChangeManager.
        :param file_change_manager: Instanca FileChangeManager klase.
        """
        self.file_change_manager = file_change_manager

    async def sync(self, usb_path, backup_folder):
        """
        Sinhronizuje fajlove sa USB-a u backup folder.
        :param usb_path: Putanja do mount point-a USB-a.
        :param backup_folder: Folder gde će se sačuvati backup.
        """
        # Kreiranje novog backup foldera
        new_backup_path = os.path.join(backup_folder, _(f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"))
        os.makedirs(new_backup_path, exist_ok=True)

        tasks = []
        for file in self.file_change_manager.new_files + self.file_change_manager.modified_files:
            src_path = os.path.join(usb_path, file)
            dest_path = os.path.join(new_backup_path, file)
            tasks.append(asyncio.to_thread(shutil.copy2, src_path, dest_path))

        await asyncio.gather(*tasks)
        print("Sinhronizacija završena.")
        
        await self.update_backup_history(new_backup_path)
        
        # Snimanje liste obrisanih fajlova
        print("----------------------------")
        deleted_files_path = os.path.join(new_backup_path, "deleted_files.json")
        print(f"putanja delete file je .... { deleted_files_path }")
        print(f"izbrisani files je .....  { self.file_change_manager.deleted_files }")
        print("----------------------------")
        with open(deleted_files_path, 'w') as f:
            json.dump(self.file_change_manager.deleted_files, f, indent=4)

        print(f"Backup završen u: {new_backup_path}")


    async def update_backup_history(self, new_backup_path):
        """
        Dodaje novu relativnu putanju bekapa u ključ `backup_history` u fajlu `.serial`.
        :param new_backup_path: Apsolutna putanja do novog backup foldera.
        """
        parent_folder = os.path.dirname(new_backup_path)
        serial_file_path = os.path.join(parent_folder, ".serial")
        relative_backup_path = os.path.relpath(new_backup_path, parent_folder)
        print(f"Serijski fajl putanja je .... {serial_file_path}")
        print(f"Relativna putanja koja se dodaje .... {relative_backup_path}")
        
        # Proveravamo da li postoji .serial fajl
        if os.path.exists(serial_file_path):
            # Učitavanje postojećeg sadržaja
            with open(serial_file_path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print("Greška prilikom čitanja .serial fajla. Kreiraće se novi podaci.")
                    data = {}
        else:
            # Ako fajl ne postoji, kreiramo novu strukturu
            data = {}

        # Osiguravamo da `backup_history` postoji kao lista
        if "backup_history" not in data:
            data["backup_history"] = []

        # Dodavanje nove relativne putanje samo ako već ne postoji
        if relative_backup_path not in data["backup_history"]:
            data["backup_history"].append(relative_backup_path)

        # Čuvanje ažuriranih podataka nazad u .serial fajl
        with open(serial_file_path, 'w') as f:
            json.dump(data, f, indent=4)
            print(f"Istorija bekapa uspešno ažurirana: {relative_backup_path}")
        
        self.file_change_manager.load_backup_history()
                                            
            