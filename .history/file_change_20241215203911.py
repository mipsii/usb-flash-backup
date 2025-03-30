import asyncio
from file_collector import FileCollector
from modern_popup_backup import ModernBackupPopup
from usb_backup_manager import USBBackupManager

from PySide6.QtWidgets import QDialog

class FileChangeManager:
    def __init__(self, backup_path, usb_path):
        """
        Inicijalizacija sa klasama za prikupljanje i upoređivanje fajlova.
        """
        self.backup_path = backup_path
        self.usb_path = usb_path
        
        self.popup = None  # Referenca na popup
        self.analyze_task = None
        self.file_collector = FileCollector(self)
        self.backup_manager = USBBackupManager(self)
      
        self.history = self.file_collector.load_backup_history()
        self.new_files = []
        self.modified_files = []
        self.deleted_files = []
        
        self.usb_files = {}
        self.backup_file = {}
        #self.analyze_changes()

        #self.initiate_backup_with_popup()

    async def initiate_backup_with_popup(self):
        # Upoređivanje fajlova
                
        print("Upoređivanje fajlova ...  initiate_backup_with_popup  ")    
        self.compare_files()
        
        self.popup = ModernBackupPopup(
            new_files=self.new_files,
            modified_files=self.modified_files,
            deleted_files=self.deleted_files
        )
        if self.popup.exec() == QDialog.DialogCode.Accepted:
            print(f"pokrenut backup............ { self.usb_path} ....  { self.backup_path}")
            asyncio.create_task(self.backup_manager.sync(self.usb_path, self.backup_path))
            asyncio.create_task(self.clear_changes())
        else:
            print("Backup otkazan.")
        asyncio.create_task(self.clear_changes())
        self.popup = None  # Resetuje referencu nakon zatvaranja popup-a

    async def gg(self):
        await self.analyze_changes()
        await self.initiate_backup_with_popup()


    async def analyze_changes(self):
        """
        Analiziranje promena između USB-a i poslednjeg backup-a.
        """
        # Prikupljanje fajlova
        print("Prikupljanje fajlova sa USB-a...")
        self.usb_files = await self.file_collector.get_usb_files(self.usb_path)
        print(f"files usb je :   {self.usb_files}")
        
        print("Prikupljanje fajlova sa poslednjeg backup-a...")
        self.backup_file =await self.backup_files()
        print(f"backup files je {self.backup_file}")

        print("skupljanje files je  završena!")
        # Upoređivanje fajlova
        print("Upoređivanje fajlova...analyze_changes")    
        #self.compare_files(usb_files, backup_files)

    def compare_files(self):
        """
        Poredi fajlove sa USB-a i iz poslednjeg backup-a.
        :param usb_files: Fajlovi sa USB-a (rečnik: {putanja: atributi}).
        :param backup_files: Fajlovi iz poslednjeg backup-a (rečnik: {putanja: atributi}).
        """
        print(f"USB files: {self.usb_files}")
        print(f"Backup files: {self.backup_file}")

        if self.backup_file is None:
            print("backup_file nije inicijalizovan! Postavljam na prazan rečnik.")
            self.backup_file = {}
        print("------------------------------")        
        print(f"USB files: {self.usb_files}")
        print(f"Backup files: {self.backup_file}")
        usb_set = set(self.usb_files.keys())
        backup_set = set(self.backup_file.keys())
        print("------------------------------")        
        # Novi fajlovi
        self.new_files = list(usb_set - backup_set)
        print(f"novi {self.new_files}")

        # Obrisani fajlovi
        self.deleted_files = list(backup_set - usb_set)
        print(f"izbrisani {self.deleted_files}")
         
        # Izmenjeni fajlovi
        self.modified_files = [
            file for file in usb_set & backup_set
            if self.usb_files[file]['modification_time'] > self.backup_file[file]['modification_time']
        ]
        print(f"izmenjeni {self.modified_files}")
    async def backup_files(self, target_index=None):
        """
        Kombinuje sve fajlove iz istorije backup-a do datog indeksa.
        :param target_index: Ciljani indeks do kog se kombinuje (podrazumevano cela istorija).
        :return: Kombinovano stanje fajlova.
        """
        
        print(f"HISTORI je { self.history}")

        #return await asyncio.to_thread(self.file_collector.recursive_backup_merge(history, target_index=target_index))
        self.backup_file = await self.file_collector.recursive_backup_merge(self.history, target_index=target_index)
        return self.backup_file
    
    def get_changes(self):
        """
        Vraća sve promene u formatu rečnika.
        """
        return {
            "new_files": self.new_files,
            "modified_files": self.modified_files,
            "deleted_files": self.deleted_files
        }

    async def clear_changes(self):
        """
        Čisti liste promena (oslobadanje memorije ako nije potrebno dalje držati informacije).
        """
        self.new_files.clear()
        self.modified_files.clear()
        self.deleted_files.clear()
        self.popup = None