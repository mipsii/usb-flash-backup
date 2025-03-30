import asyncio
import json
import os
from unittest import signals
from file_collector import FileCollector
from modern_popup_backup import ModernBackupPopup
from signal_manager import SignalManager
from usb_backup_manager import USBBackupManager
from PySide6.QtCore import Signal, QObject, QTimer

from PySide6.QtWidgets import QDialog

class FileChangeManager(QObject):
    

    def __init__(self, backup_path, usb_path):
        """
        Inicijalizacija sa klasama za prikupljanje i upoređivanje fajlova.
        """
        super().__init__()  # Pozivanje konstruktora bazne klase (QObject)
        self.signal_manager = SignalManager()
        self.backup_path = backup_path
        self.usb_path = usb_path
        self._history = []
        self.popup = None  # Referenca na popup
        self.analyze_task = None
        self.file_collector = FileCollector()
        self.backup_manager = USBBackupManager(self)

        self.new_files = []
        self.modified_files = []
        self.deleted_files = []
        
        self.usb_files = {}
        self.backup_file = {}
        self.spisak()
        self._signals()
        
        #self.analyze_changes()

        #self.initiate_backup_with_popup()
    def _signals(self):
        self.signal_manager = SignalManager()
        self.signal_manager.connect_signal_async("analyze_files", self,  "analyze_changes" )

    def spisak(self):
        self.history = self.load_backup_history()
       
    @property
    def history(self):
        return self._history
        
    @history.setter
    def history(self, value):
        if self._history != value:
            self._history = value
            QTimer.singleShot(0, lambda: self.history_changed.emit(self._history))
            QTimer.singleShot(0, lambda: self.signal_manager.emit_signal("history_changed",self._history))
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
            asyncio.create_task(self.backup_manager.sync(self.usb_path, self.backup_path))
            #asyncio.create_task(self.clear_changes())
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
        print("------------------------------")     
        if self.usb_path:
            self.usb_files = await self.file_collector.get_usb_files(self.usb_path)
            print(f"files usb je :   {self.usb_files}")
            print("------------------------------")   
        else:
            print(f"Usb nije aktivan")  
        
        print("Prikupljanje fajlova sa poslednjeg backup-a...")
        self.backup_file =await self.backup_files()
        print(f"backup files je {self.backup_file}")
        print("------------------------------")     
        print("skupljanje files je  završena!")

    def compare_files(self):
        """
        :param usb_files: Fajlovi sa USB-a (rečnik: {putanja: atributi}).
        :param backup_files: Fajlovi iz poslednjeg backup-a (rečnik: {putanja: atributi}).
        """
        if self.backup_file is None:
            print("backup_file nije inicijalizovan! Postavljam na prazan rečnik.")
            self.backup_file = {}
        print("------------------------------")        
        print(f"USB files: {self.usb_files}")
        print("------------------------------")  
        print(f"Backup files: {self.backup_file}")
        usb_set = set(self.usb_files.keys())
        backup_set = set(self.backup_file.keys())
        print("------------------------------")        
        # Novi fajlovi
        self.new_files = list(usb_set - backup_set)
        print(f"novi {self.new_files}")
        print("------------------------------")  
        # Obrisani fajlovi
        self.deleted_files = list(backup_set - usb_set)
        print(f"izbrisani {self.deleted_files}")
        print("------------------------------")  
        # Izmenjeni fajlovi
        self.modified_files = [
            file for file in usb_set & backup_set
            if self.usb_files[file]['modification_time'] > self.backup_file[file]['modification_time']
        ]
        print(f"izmenjeni {self.modified_files}")
        print("------------------------------")  
        
    async def backup_files(self, target_index=None):
        """
        Kombinuje sve fajlove iz istorije backup-a do datog indeksa.
        :param target_index: Ciljani indeks do kog se kombinuje (podrazumevano cela istorija).
        :return: Kombinovano stanje fajlova.
        """
        #return await asyncio.to_thread(self.file_collector.recursive_backup_merge(history, target_index=target_index))
        self.backup_file = await self.file_collector.recursive_backup_merge(self._history["backup_path"], self._history["backup_history"], target_index=target_index)
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

    def load_backup_history(self):
        """
        Učitaj istoriju backup-a iz fajla `.serial`.
        Pretpostavlja JSON format sa ključem `backup_history`.
        """
        serial_file_path = os.path.join(self.backup_path,".serial")
        result = {
            "backup_path": self.backup_path,  # Putanja na prvom mestu
            "backup_history": []
        }
    
        if os.path.exists(serial_file_path):
            with open(serial_file_path, "r") as f:
                data = json.load(f)
                result["backup_history"] = data.get("backup_history", [])

        return result
    
    async def clear_changes(self):
        """
        Čisti liste promena (oslobadanje memorije ako nije potrebno dalje držati informacije).
        """
        self.new_files.clear()
        self.modified_files.clear()
        self.deleted_files.clear()
        self.popup = None