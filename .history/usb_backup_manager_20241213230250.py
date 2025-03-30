import asyncio
from datetime import datetime
import json
import os
import shutil


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
        new_backup_path = os.path.join(backup_folder, f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
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
        deleted_files_path = os.path.join(new_backup_path, "deleted_files.json")
        with open(deleted_files_path, 'w') as f:
            json.dump(self.file_change_manager.deleted_files, f, indent=4)

        print(f"Backup završen u: {new_backup_path}")

    async def update_backup_history(self, new_backup_path):
        parent_folder = os.path.dirname(new_backup_path)
        serial_file_path = os.path.join(parent_folder, ".serial")
        print(f"Serijski fajl putanja je .... { serial_file_path }")
        # Proveravamo da li postoji serial fajl
        if os.path.exists(serial_file_path):
            data["backup_history"].append(os.path.relpath(new_backup_path, parent_folder))
            # Čuvanje ažuriranih podataka nazad u .serial
            with open(serial_file_path, 'w') as f:
                json.dump(data, f, indent=4)
                print(f"Istorija bekapa uspešno ažurirana: {new_backup_path}")
                                        
        